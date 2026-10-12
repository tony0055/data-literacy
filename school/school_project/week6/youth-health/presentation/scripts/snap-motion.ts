import { mkdir } from "node:fs/promises";
import { join } from "node:path";

const root = join(import.meta.dir, "..");
const outDir = join(root, "renders", "motion");
const slidesToSnap = (Bun.argv.slice(2)[0] ?? "5,8,11").split(",").map(Number);
const fractions = [0, 0.4, 1];

const server = Bun.serve({
  port: 0,
  hostname: "127.0.0.1",
  async fetch(req) {
    const file = Bun.file(join(root, decodeURIComponent(new URL(req.url).pathname)));
    return (await file.exists()) ? new Response(file) : new Response("not found", { status: 404 });
  },
});
const base = `http://127.0.0.1:${server.port}/index.html`;
const view = new Bun.WebView({ width: 1920, height: 1080, backend: "chrome" });
await view.navigate(`${base}?slide=1&anim=1`);
await view.cdp("Emulation.setDeviceMetricsOverride", { width: 1920, height: 1080, deviceScaleFactor: 1, mobile: false });
const settle = () => view.evaluate("document.fonts.ready");

await mkdir(outDir, { recursive: true });
const report: Record<string, unknown> = {};

for (const n of slidesToSnap) {
  for (const f of fractions) {
    await view.navigate(`${base}?slide=${n}&anim=${f}`);
    await settle();
    await Bun.write(join(outDir, `slide-${String(n).padStart(2, "0")}-at-${String(f).replace(".", "_")}.png`), await view.screenshot());
  }
  await view.navigate(`${base}?slide=${n}&anim=1`);
  await settle();
  report[`slide${n}`] = JSON.parse(await view.evaluate(`(() => {
    const s = document.querySelector('.slide:not([hidden])');
    const sowe = s.querySelector('.sowe');
    const bar = s.querySelector('.chart svg rect');
    const line = s.querySelector('.chart svg polyline');
    const g = (el) => el ? getComputedStyle(el) : null;
    return JSON.stringify({
      soweOpacity: sowe ? g(sowe).opacity : null,
      barTransform: bar ? g(bar).transform : null,
      lineDashOffset: line ? g(line).strokeDashoffset : null,
      timelineCount: window.__motion.timelines.length,
      allAtEnd: window.__motion.timelines.every(e => e.tl.currentTime >= e.tl.duration - 1),
    });
  })()`));
}

await view.navigate(`${base}?slide=5&anim=0`);
await settle();
report.startState = JSON.parse(await view.evaluate(`(() => {
  const s = document.querySelector('.slide:not([hidden])');
  const sowe = s.querySelector('.sowe');
  const bar = s.querySelector('.chart svg rect');
  return JSON.stringify({ soweOpacity: getComputedStyle(sowe).opacity, barTransform: getComputedStyle(bar).transform });
})()`));

await view.cdp("Emulation.setEmulatedMedia", { features: [{ name: "prefers-reduced-motion", value: "reduce" }] });
await view.navigate(`${base}?slide=5`);
await settle();
await Bun.write(join(outDir, "slide-05-reduced-motion.png"), await view.screenshot());
report.reducedMotion = JSON.parse(await view.evaluate(`(() => {
  const s = document.querySelector('.slide:not([hidden])');
  return JSON.stringify({
    soweOpacity: getComputedStyle(s.querySelector('.sowe')).opacity,
    allAtEnd: window.__motion.timelines.every(e => e.tl.currentTime >= e.tl.duration - 1),
  });
})()`));

view.close();
server.stop();
console.log(JSON.stringify({ outDir, snapped: slidesToSnap, fractions, report }, null, 1));
