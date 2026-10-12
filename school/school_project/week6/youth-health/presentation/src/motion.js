const { createTimeline, createDrawable, stagger, utils } = window.anime;

const motionQuery = new URLSearchParams(location.search);
const motionSlides = [...document.querySelectorAll(".slide")];
const reduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
const motionRenderMode = motionQuery.has("check") || motionQuery.has("slide");
const seekParam = motionQuery.get("anim");

const ENTER = { opacity: [0, 1], translateY: [16, 0] };
const STEP = 520;

const pick = (root, sel) => [...root.querySelectorAll(sel)];

function buildSlide(slide) {
  const tl = createTimeline({ autoplay: false, defaults: { duration: STEP, ease: "out(3)" } });
  const primers = [];
  let at = 0;

  const addStep = (targets, params, gap = 240) => {
    if (!targets || targets.length === 0) return;
    const from = {};
    for (const [k, v] of Object.entries(params)) if (Array.isArray(v) && v.length === 2) from[k] = v[0];
    if (Object.keys(from).length) primers.push(() => utils.set(targets, from));
    tl.add(targets, params, at);
    at += gap;
  };

  addStep(pick(slide, ".head > *"), { ...ENTER, delay: stagger(80) }, 360);

  const charts = pick(slide, ".chart");
  const plainBlocks = pick(slide, ".body .grid > *, .body > .stack > *, .body > .ask, .body > .vs > *, .body > .tone")
    .filter((el) => !el.closest(".chart") && !charts.includes(el));

  for (const chart of charts) {
    addStep(pick(chart, ".chart-title, .chart-sub"), { ...ENTER }, 180);
    addStep(pick(chart, "svg .grid line, svg .base, svg .tick, svg .alab:not(.slab), svg .clab"), { opacity: [0, 1], delay: stagger(18) }, 300);

    const bars = pick(chart, "svg rect");
    const lines = pick(chart, "svg polyline");
    const dots = pick(chart, "svg circle");
    if (bars.length) addStep(bars, { scaleY: [0, 1], duration: 720, delay: stagger(70) }, 720 + 70 * bars.length);
    if (lines.length) addStep(lines.map((l) => createDrawable(l)), { draw: ["0 0", "0 1"], duration: 900, delay: stagger(140) }, 900 + 140 * (lines.length - 1));
    if (dots.length) addStep(dots, { scale: [0, 1], duration: 380, delay: stagger(50) }, 380 + 50 * dots.length);
    addStep(pick(chart, "svg .slab"), { opacity: [0, 1], delay: stagger(60) }, 240);
    addStep(pick(chart, "svg .vlab:not(.slab)"), { opacity: [0, 1], delay: stagger(50) }, 280);
    addStep(pick(chart, "svg .note, .chart-note"), { ...ENTER }, 220);
    addStep(pick(chart, ".chart-src"), { opacity: [0, 1] }, 160);
  }

  addStep(plainBlocks, { ...ENTER, delay: stagger(110) }, 320);
  addStep(pick(slide, ".sowe"), { ...ENTER }, 0);

  return { tl, prime: () => primers.forEach((f) => f()) };
}

const timelines = motionSlides.map((slide) => ({ slide, ...buildSlide(slide), played: false }));
const seekTo = (f) => timelines.forEach((e) => e.tl.seek(e.tl.duration * Math.max(0, Math.min(1, f))));

if (reduced || motionRenderMode || seekParam !== null) {
  const f = seekParam === null ? 1 : Number(seekParam);
  timelines.forEach((e) => e.prime());
  if (f > 0) seekTo(f);
  timelines.forEach((e) => { e.played = true; });
} else {
  timelines.forEach((e) => e.prime());

  const play = (e) => { e.played = true; e.tl.restart(); };
  const io = new IntersectionObserver((entries) => {
    for (const en of entries) {
      if (!en.isIntersecting) continue;
      const e = timelines.find((x) => x.slide === en.target);
      if (e && !e.played) play(e);
    }
  }, { threshold: 0.45 });
  for (const e of timelines) io.observe(e.slide);

  const replay = () => { const e = timelines[window.__deckCurrentSlide()]; if (e) { e.prime(); play(e); } };

  document.addEventListener("keydown", (ev) => {
    if (ev.metaKey || ev.ctrlKey || ev.altKey) return;
    if (ev.key === "r" || ev.key === "R") { ev.preventDefault(); replay(); }
  });

  const btn = document.createElement("button");
  btn.className = "replay-btn";
  btn.type = "button";
  btn.textContent = "다시 재생 (R)";
  btn.addEventListener("click", replay);
  document.body.append(btn);

  window.addEventListener("beforeprint", () => seekTo(1));
}

window.__motion = { timelines, seekAll: seekTo };
