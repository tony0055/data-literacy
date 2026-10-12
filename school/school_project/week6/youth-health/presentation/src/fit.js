window.__jsErrors = [];
window.addEventListener("error", (e) => window.__jsErrors.push(`${e.message} @ ${(e.filename || "").split("/").pop()}:${e.lineno}`));
window.addEventListener("unhandledrejection", (e) => window.__jsErrors.push(`unhandled rejection: ${e.reason}`));

window.__deckCurrentSlide = () => {
  const all = [...document.querySelectorAll(".slide")];
  const mid = window.innerHeight / 2;
  let best = 0;
  let bestDist = Infinity;
  for (const [i, s] of all.entries()) {
    const r = s.getBoundingClientRect();
    if (r.height === 0) continue;
    const d = Math.abs(r.top + r.height / 2 - mid);
    if (d < bestDist) { bestDist = d; best = i; }
  }
  return best;
};

const deck = document.querySelector(".deck");
const fitParams = new URLSearchParams(location.search);
const soloSlide = Number(fitParams.get("slide"));

if (soloSlide) {
  document.body.classList.add("solo");
  document.querySelectorAll(".slide").forEach((s, i) => { s.hidden = i + 1 !== soloSlide; });
} else {
  const fit = () => { deck.style.zoom = Math.min(1, (window.innerWidth - 64) / 1920); };
  window.addEventListener("resize", fit);
  window.addEventListener("beforeprint", () => { deck.style.zoom = 1; });
  window.addEventListener("afterprint", fit);
  if (!fitParams.has("check")) fit();
}

if (fitParams.has("check")) {
  const BODY_FLOOR = 18;
  const HARD_FLOOR = 14;
  const TERTIARY = ".kicker, .kicker *, .eyebrow, .foot, .foot *, .tag, .chart-src, .chart-src *, .chart-sub, .legend, .legend *, .meta, .p-no, .chip, .idx, .key .k, .tone th, [data-type-ok], [data-type-ok] *";
  const CLIPPABLE = ".body, .card, .stack, .chart, .ask, .key, .eq, .vs, [data-check-fit]";

  document.fonts.ready.then(() => {
    const label = (el) => `${el.tagName.toLowerCase()}.${[...el.classList].join(".")} "${(el.textContent || "").trim().slice(0, 24)}"`;
    const lineCount = (el) => {
      const lh = parseFloat(getComputedStyle(el).lineHeight);
      return Number.isFinite(lh) && lh > 0 ? Math.round(el.getBoundingClientRect().height / lh) : 0;
    };

    const slides = [...document.querySelectorAll(".slide")].map((s, i) => {
      const r = s.getBoundingClientRect();
      const over = [...s.querySelectorAll("*")].filter((el) => {
        const b = el.getBoundingClientRect();
        return b.width > 0 && (b.right > r.right + 1 || b.bottom > r.bottom + 1 || b.left < r.left - 1 || b.top < r.top - 1);
      }).slice(0, 6).map(label);

      const clipped = [...s.querySelectorAll(CLIPPABLE)]
        .filter((el) => el.scrollHeight > el.clientHeight + 2 || el.scrollWidth > el.clientWidth + 2)
        .slice(0, 6).map((el) => `${label(el)} +${el.scrollHeight - el.clientHeight}h +${el.scrollWidth - el.clientWidth}w`);

      const tiny = [...s.querySelectorAll("*")].filter((el) => {
        if (!el.firstChild || el.firstChild.nodeType !== 3 || !el.textContent.trim()) return false;
        const px = parseFloat(getComputedStyle(el).fontSize);
        if (px < HARD_FLOOR) return true;
        return px < BODY_FLOOR && !el.matches(TERTIARY) && !(el.parentElement && el.parentElement.matches(".sowe"));
      }).slice(0, 6).map((el) => `${label(el)} ${getComputedStyle(el).fontSize}`);

      const head = s.querySelector(".headline");
      return { n: i + 1, over, clipped, headLines: head ? lineCount(head) : 0, tiny };
    }).filter((x) => x.over.length || x.clipped.length || x.headLines > 1 || x.tiny.length);

    const report = window.__jsErrors.length ? [{ jsErrors: window.__jsErrors }, ...slides] : slides;
    const pre = document.createElement("pre");
    pre.id = "report";
    pre.textContent = JSON.stringify(report);
    document.body.append(pre);
  });
}
