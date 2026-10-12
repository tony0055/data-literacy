import { mkdir } from "node:fs/promises";
import { join } from "node:path";

const root = join(import.meta.dir, "..");
const [page = "index.html", ...flags] = Bun.argv.slice(2);
const pdfPath = flags.includes("--pdf") ? join(root, "renders", page.replace(/\.html$/, ".pdf")) : null;
const outDir = join(root, "renders", page.replace(/\.html$/, ""));

const server = Bun.serve({
  port: 0,
  hostname: "127.0.0.1",
  async fetch(req) {
    const file = Bun.file(join(root, decodeURIComponent(new URL(req.url).pathname)));
    return (await file.exists()) ? new Response(file) : new Response("not found", { status: 404 });
  },
});
const base = `http://127.0.0.1:${server.port}/${page}`;
const view = new Bun.WebView({ width: 1920, height: 1080, backend: "chrome" });

const settle = () => view.evaluate(
  "document.fonts.ready.then(() => Promise.all([...document.images].map((im) => im.complete ? 1 : new Promise((r) => { im.onload = im.onerror = r; }))))",
);

await view.navigate(`${base}?check=1`);
await view.cdp("Emulation.setDeviceMetricsOverride", { width: 1920, height: 1080, deviceScaleFactor: 1, mobile: false });
await view.navigate(`${base}?check=1`);
let report: string | null = null;
for (let i = 0; i < 50 && !report; i++) {
  report = await view.evaluate("document.getElementById('report')?.textContent || null");
  if (!report) await Bun.sleep(100);
}
const count = Number(await view.evaluate("document.querySelectorAll('.slide').length"));

await mkdir(outDir, { recursive: true });
for (let n = 1; n <= count; n++) {
  await view.navigate(`${base}?slide=${n}`);
  await settle();
  await Bun.write(join(outDir, `slide-${String(n).padStart(2, "0")}.png`), await view.screenshot());
}

if (pdfPath) {
  await view.navigate(base);
  await settle();
  const { data } = await view.cdp("Page.printToPDF", { preferCSSPageSize: true, printBackground: true });
  await Bun.write(pdfPath, Buffer.from(data, "base64"));
}

view.close();
server.stop();
console.log(JSON.stringify({ slides: count, outDir, pdf: pdfPath, issues: JSON.parse(report ?? "null") }, null, 1));
