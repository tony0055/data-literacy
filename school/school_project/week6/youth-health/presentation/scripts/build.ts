import { join } from "node:path";

const root = join(import.meta.dir, "..");
const dataPath = join(root, "..", "chart-data.json");
const htmlPath = join(root, "index.html");

const raw = await Bun.file(dataPath).text();
const data = JSON.parse(raw);
const embedded = JSON.stringify(data);

const html = await Bun.file(htmlPath).text();
const open = `<script type="application/json" id="chart-data">`;
const start = html.indexOf(open);
if (start < 0) throw new Error("chart-data block not found in index.html");
const from = start + open.length;
const to = html.indexOf("</script>", from);

const next = html.slice(0, from) + embedded + html.slice(to);
await Bun.write(htmlPath, next);

const keys = Object.keys(data).filter((k) => !k.startsWith("_"));
const used = [...html.matchAll(/data-chart="([^"]+)"/g)].map((m) => m[1]);
const missing = used.filter((k) => !keys.includes(k));

console.log(JSON.stringify({
  injectedBytes: embedded.length,
  datasets: keys.length,
  chartsInDeck: used.length,
  missingDatasets: missing,
  sha256: new Bun.CryptoHasher("sha256").update(embedded).digest("hex").slice(0, 16),
}, null, 1));
if (missing.length) process.exit(1);
