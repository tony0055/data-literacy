import { join } from "node:path";

const root = join(import.meta.dir, "..");
const proj = join(root, "..");

const numbersIn = (s: string) => new Set((s.match(/\d+(?:\.\d+)?/g) ?? []).map((n) => String(Number(n))));

const sources = ["chart-data.json", "verification.md", "claims.csv", "report.md"];
const allowed = new Set<string>();
for (const f of sources) for (const n of numbersIn(await Bun.file(join(proj, f)).text())) allowed.add(n);
for (const n of numbersIn(await Bun.file(join(proj, "research", "context-counterevidence.md")).text())) allowed.add(n);

const html = await Bun.file(join(root, "index.html")).text();
const prose = html
  .replace(/<script[\s\S]*?<\/script>/g, " ")
  .replace(/<style[\s\S]*?<\/style>/g, " ")
  .replace(/<[^>]+>/g, " ");

const STRUCTURAL = new Set(["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "20", "30", "40", "50", "60", "70", "80", "90", "100"]);

const found = [...numbersIn(prose)];
const unverified = found.filter((n) => !allowed.has(n) && !STRUCTURAL.has(n));

console.log(JSON.stringify({
  numbersInDeck: found.length,
  allowedFromSources: allowed.size,
  unverified,
}, null, 1));
if (unverified.length) {
  console.error("\n덱 본문에 있으나 원본 파일에서 찾지 못한 수치:", unverified.join(", "));
  process.exit(1);
}
