import { join } from "node:path";

const root = join(import.meta.dir, "..");
const width = Number(Bun.argv.slice(2)[0] ?? 1512);
const height = Number(Bun.argv.slice(2)[1] ?? 900);

const server = Bun.serve({
  port: 0,
  hostname: "127.0.0.1",
  async fetch(req) {
    const file = Bun.file(join(root, decodeURIComponent(new URL(req.url).pathname)));
    return (await file.exists()) ? new Response(file) : new Response("not found", { status: 404 });
  },
});

const url = `http://127.0.0.1:${server.port}/index.html`;
const view = new Bun.WebView({ width, height, backend: "chrome" });
await view.navigate(url);
await view.cdp("Emulation.setDeviceMetricsOverride", { width, height, deviceScaleFactor: 1, mobile: false });
await view.navigate(url);
await view.evaluate("document.fonts.ready");

const geometry = JSON.parse(await view.evaluate(`(() => {
  const slides = [...document.querySelectorAll(".slide")];
  const rows = [];
  for (let k = 0; k < slides.length; k++) {
    slides[k].scrollIntoView({ block: "start" });
    rows.push({ scrolledTo: k + 1, reported: window.__deckCurrentSlide() + 1 });
  }
  return JSON.stringify({
    zoom: getComputedStyle(document.querySelector(".deck")).zoom,
    mismatches: rows.filter((r) => r.scrolledTo !== r.reported),
    checked: rows.length,
  });
})()`));

const walk = JSON.parse(await view.evaluate(`(async () => {
  const slides = [...document.querySelectorAll(".slide")];
  const settle = () => new Promise((resolve) => {
    let last = -1;
    let same = 0;
    let frames = 0;
    const tick = () => {
      const y = Math.round(window.scrollY);
      same = y === last ? same + 1 : 0;
      last = y;
      if (same >= 5 || ++frames > 240) return resolve();
      requestAnimationFrame(tick);
    };
    requestAnimationFrame(tick);
  });
  const press = async (key) => {
    document.dispatchEvent(new KeyboardEvent("keydown", { key, bubbles: true, cancelable: true }));
    await settle();
  };
  window.scrollTo(0, 0);
  await settle();
  const down = [window.__deckCurrentSlide() + 1];
  for (let i = 0; i < slides.length + 1; i++) { await press("ArrowDown"); down.push(window.__deckCurrentSlide() + 1); }
  const up = [];
  for (let i = 0; i < 4; i++) { await press("ArrowUp"); up.push(window.__deckCurrentSlide() + 1); }
  return JSON.stringify({ down, up, total: slides.length });
})()`));

view.close();
server.stop();

const expectedDown = Array.from({ length: walk.total + 2 }, (_, i) => Math.min(i + 1, walk.total));
const downOk = JSON.stringify(walk.down) === JSON.stringify(expectedDown);
const upOk = JSON.stringify(walk.up) === JSON.stringify([walk.total - 1, walk.total - 2, walk.total - 3, walk.total - 4]);

console.log(JSON.stringify({ window: { width, height }, geometry, walk, downOk, upOk }, null, 1));
process.exit(geometry.mismatches.length === 0 && downOk && upOk ? 0 : 1);
