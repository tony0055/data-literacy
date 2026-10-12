const slides = [...document.querySelectorAll(".slide")];
const presentQuery = new URLSearchParams(location.search);

slides.forEach((s, i) => {
  const n = s.querySelector(".pg b");
  const t = s.querySelector(".pg .tot");
  if (n) n.textContent = String(i + 1);
  if (t) t.textContent = String(slides.length);
});

const renderMode = presentQuery.has("check") || presentQuery.has("slide");

if (!renderMode) {
  const deck = document.querySelector(".deck");
  const go = (d) => {
    const i = Math.min(slides.length - 1, Math.max(0, window.__deckCurrentSlide() + d));
    slides[i].scrollIntoView({ behavior: "smooth", block: "start" });
  };
  const fit = () => { deck.style.zoom = Math.min(1, (window.innerWidth - 64) / 1920); };

  document.addEventListener("keydown", (e) => {
    if (e.metaKey || e.ctrlKey || e.altKey) return;
    const k = e.key;
    if (k === "ArrowRight" || k === "ArrowDown" || k === "PageDown" || k === " ") { e.preventDefault(); go(1); }
    else if (k === "ArrowLeft" || k === "ArrowUp" || k === "PageUp") { e.preventDefault(); go(-1); }
    else if (k === "Home") { e.preventDefault(); slides[0].scrollIntoView(); }
    else if (k === "End") { e.preventDefault(); slides.at(-1).scrollIntoView(); }
    else if (k === "f" || k === "F") { document.fullscreenElement ? document.exitFullscreen() : document.documentElement.requestFullscreen(); }
    else if (k === "Escape") {
      e.preventDefault();
      const on = document.body.classList.toggle("overview");
      if (on) { deck.style.zoom = ""; } else { fit(); }
    }
  });

  document.addEventListener("click", (e) => {
    if (!document.body.classList.contains("overview")) return;
    const s = e.target.closest(".slide");
    if (!s) return;
    document.body.classList.remove("overview");
    fit();
    s.scrollIntoView({ block: "start" });
  });
}
