const DATA = JSON.parse(document.getElementById("chart-data").textContent);
const NS = "http://www.w3.org/2000/svg";

const el = (name, attrs = {}, text) => {
  const n = document.createElementNS(NS, name);
  for (const [k, v] of Object.entries(attrs)) n.setAttribute(k, String(v));
  if (text !== undefined) n.textContent = String(text);
  return n;
};

const axisOf = (max) => {
  const need = max * 1.02;
  const mag = Math.pow(10, Math.floor(Math.log10(need)) - 1);
  let best = null;
  for (const n of [4, 5, 6]) {
    for (const m of [1, 2, 2.5, 5, 10, 20, 25, 50, 100]) {
      const step = m * mag;
      const top = step * n;
      if (top >= need && (!best || top < best.top)) best = { top, n };
    }
  }
  return best ?? { top: need, n: 4 };
};

const decimalsOf = (values) => Math.max(...values.map((v) => (String(v).split(".")[1] ?? "").length));
const fmtWith = (d) => (v) => v.toFixed(d);

const ticksOf = (top, want) => Array.from({ length: want + 1 }, (_, i) => Number(((i * top) / want).toPrecision(6)));

const TONE = { worse: ["b-worse", "l-worse", "note"], evid: ["b-evid", "l-evid", "alab"], better: ["b-better", "l-better", "alab"], neutral: ["b-neutral", "l-neutral", "alab"] };
const toneOf = (s) => TONE[s.색 ?? (s.강조 ? "worse" : "neutral")] ?? TONE.neutral;

function frame(svg, { x0, x1, yTop, yBase, top, unit, steps }) {
  const g = el("g", { class: "grid" });
  for (const t of ticksOf(top, steps)) {
    const y = yBase - (t / top) * (yBase - yTop);
    if (t > 0) g.append(el("line", { x1: x0, y1: y, x2: x1, y2: y }));
    svg.append(el("text", { class: "tick", x: x0 - 12, y: y + 6, "text-anchor": "end" }, String(t)));
  }
  svg.append(g);
  svg.append(el("line", { class: "base", x1: x0, y1: yBase, x2: x1, y2: yBase }));
  if (unit) svg.append(el("text", { class: "alab", x: x0 - 56, y: yBase + 64 }, `단위: ${unit}`));
}

function bar(d, W) {
  const H = 400, x0 = 84, x1 = W - 16, yTop = 44, yBase = H - 80;
  const svg = el("svg", { viewBox: `0 0 ${W} ${H}`, role: "img", "aria-label": d.제목 });
  const vals = d.bars.map((b) => b.value);
  const fmt = fmtWith(decimalsOf(vals));
  const { top, n: steps } = axisOf(Math.max(...vals));
  frame(svg, { x0, x1, yTop, yBase, top, unit: d.단위, steps });
  const gw = (x1 - x0) / d.bars.length;
  const bw = Math.min(112, gw - 24);
  for (const [i, b] of d.bars.entries()) {
    const cx = x0 + gw * (i + 0.5);
    const h = (b.value / top) * (yBase - yTop);
    svg.append(el("rect", { class: b.강조 ? "b-worse" : "b-neutral", x: cx - bw / 2, y: yBase - h, width: bw, height: h }));
    svg.append(el("text", { class: "vlab", x: cx, y: yBase - h - 12, "text-anchor": "middle" }, fmt(b.value)));
    svg.append(el("text", { class: `${b.강조 ? "note" : "alab"} clab`, x: cx, y: yBase + 32, "text-anchor": "middle" }, b.key));
  }
  return svg;
}

function changePairs(d, W) {
  const H = 400, x0 = 84, x1 = W - 16, yTop = 44, yBase = H - 104;
  const svg = el("svg", { viewBox: `0 0 ${W} ${H}`, role: "img", "aria-label": d.제목 });
  const vals = d.series.flatMap((s) => s.points.map((p) => p.value));
  const fmt = fmtWith(decimalsOf(vals));
  const { top, n: steps } = axisOf(Math.max(...vals));
  frame(svg, { x0, x1, yTop, yBase, top, unit: d.단위, steps });
  const gw = (x1 - x0) / d.series.length;
  const bw = Math.min(96, (gw - 96) / 2);
  for (const [gi, s] of d.series.entries()) {
    const [fill, , label] = toneOf(s);
    const cx = x0 + gw * (gi + 0.5);
    const start = cx - (bw * s.points.length + 16) / 2;
    for (const [i, p] of s.points.entries()) {
      const h = (p.value / top) * (yBase - yTop);
      const x = start + (bw + 16) * i;
      svg.append(el("rect", { class: i === s.points.length - 1 ? fill : "b-neutral", x, y: yBase - h, width: bw, height: h }));
      svg.append(el("text", { class: "vlab", x: x + bw / 2, y: yBase - h - 12, "text-anchor": "middle" }, fmt(p.value)));
      svg.append(el("text", { class: "alab", x: x + bw / 2, y: yBase + 32, "text-anchor": "middle" }, p.year ?? p.period));
    }
    svg.append(el("text", { class: `${label === "note" ? "note" : "vlab"} slab`, x: cx, y: yBase + 68, "text-anchor": "middle" }, s.key));
  }
  return svg;
}

function line(d, W) {
  const H = 400, x0 = 92, x1 = W - 156, yTop = 44, yBase = H - 80;
  const svg = el("svg", { viewBox: `0 0 ${W} ${H}`, role: "img", "aria-label": d.제목 });
  const series = d.series ?? [{ key: "", 강조: true, points: d.points }];
  const xsRaw = series[0].points.map((p) => p.year ?? p.period);
  const numeric = xsRaw.every((v) => typeof v === "number");
  const lo = numeric ? Math.min(...xsRaw) : 0;
  const hi = numeric ? Math.max(...xsRaw) : xsRaw.length - 1;
  const vals = series.flatMap((s) => s.points.map((p) => p.value));
  const fmt = fmtWith(decimalsOf(vals));
  const { top, n: steps } = axisOf(Math.max(...vals));
  frame(svg, { x0, x1, yTop, yBase, top, unit: d.단위, steps });

  const px = (v, i) => (numeric ? x0 + ((v - lo) / (hi - lo)) * (x1 - x0) : x0 + ((x1 - x0) / (xsRaw.length - 1)) * i);
  const py = (v) => yBase - (v / top) * (yBase - yTop);

  const peak = series[0].points.map((_, i) => Math.max(...series.map((s) => s.points[i].value)));
  for (const s of series) {
    const [dot, stroke, label] = toneOf(s);
    const pts = s.points.map((p, i) => `${px(p.year ?? p.period, i)},${py(p.value)}`).join(" ");
    svg.append(el("polyline", { class: stroke, points: pts }));
    for (const [i, p] of s.points.entries()) {
      const X = px(p.year ?? p.period, i);
      svg.append(el("circle", { class: dot, cx: X, cy: py(p.value), r: 7 }));
      const dy = p.value === peak[i] ? -18 : 30;
      svg.append(el("text", { class: "vlab", x: X, y: py(p.value) + dy, "text-anchor": "middle" }, fmt(p.value)));
    }
    const last = s.points.at(-1);
    if (s.key) svg.append(el("text", { class: `${label} slab`, x: px(last.year ?? last.period, s.points.length - 1) + 18, y: py(last.value) + 6 }, s.key));
  }
  for (const [i, x] of xsRaw.entries()) svg.append(el("text", { class: "alab", x: px(x, i), y: yBase + 32, "text-anchor": "middle" }, x));
  if (numeric) svg.append(el("text", { class: "alab", x: x1, y: yBase + 64, "font-size": "15", "text-anchor": "end" }, `가로축 = 실제 연도 간격 (${lo}~${hi})`));
  return svg;
}

const KINDS = { bar, line, "change-pairs": changePairs };

for (const host of document.querySelectorAll("[data-chart]")) {
  const d = DATA[host.dataset.chart];
  if (!d) { host.append(Object.assign(document.createElement("p"), { className: "chart-src", textContent: `데이터 없음: ${host.dataset.chart}` })); continue; }
  host.prepend(KINDS[host.dataset.kind](d, Number(host.dataset.w || 784)));
}
