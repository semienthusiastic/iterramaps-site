/* Iterra Maps — site script
   1. Hero: a looping mini version of the product (route draws, van drives, signs pop up, distance counts).
   2. Showreel: filters; draws each card's route when it scrolls into view; plays a video if a card has one.
   3. Forms: send to Formspree when FORM_ENDPOINT is set, otherwise open the visitor's email app. */

// ---- Settings -------------------------------------------------------------
// Paste your Formspree endpoint here (e.g. "https://formspree.io/f/abcdwxyz"). Leave empty to use email instead.
const FORM_ENDPOINT = "https://formspree.io/f/xyekdlbg";
const CONTACT_EMAIL = "hello@iterramaps.com";

const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
document.querySelectorAll(".js-year").forEach(el => { el.textContent = new Date().getFullYear(); });

// ---- 1. Hero demo -----------------------------------------------------------
(function heroDemo() {
  const svg = document.getElementById("demo");
  if (!svg) return;
  const trail = svg.querySelector("#trail"), glow = svg.querySelector("#trail-glow");
  const van = svg.querySelector("#van"), vanBody = svg.querySelector("#van-body");
  const stops = [...svg.querySelectorAll("#stops circle")], signs = [...svg.querySelectorAll(".sign")];
  const distEl = svg.querySelector("#dist"), legEl = svg.querySelector("#legtext"), bar = document.getElementById("progress");
  const L = trail.getTotalLength();
  const names = ["Athlone", "Galway", "Clifden", "Westport"];
  const km = [0, 90, 170, 240]; // cumulative road distance at each stop

  // where each stop sits along the drawn path
  const stopLen = stops.map(c => {
    const x = +c.getAttribute("cx"), y = +c.getAttribute("cy");
    let best = 0, bd = Infinity;
    for (let s = 0; s <= L; s += 2) { const p = trail.getPointAtLength(s), d = (p.x - x) ** 2 + (p.y - y) ** 2; if (d < bd) { bd = d; best = s; } }
    return best;
  });
  stopLen[0] = 0; stopLen[3] = L;

  // schedule (seconds): hold, leg, pause, leg, pause, leg, hold
  const HOLD0 = 0.8, LEG = [2.2, 2.2, 2.4], PAUSE = 0.6, HOLD1 = 2.4;
  const legStart = [HOLD0, HOLD0 + LEG[0] + PAUSE, HOLD0 + LEG[0] + PAUSE + LEG[1] + PAUSE];
  const TOTAL = legStart[2] + LEG[2] + HOLD1;
  const ease = u => u < 0.5 ? 2 * u * u : 1 - Math.pow(-2 * u + 2, 2) / 2;
  [trail, glow].forEach(p => { p.style.strokeDasharray = `${L} ${L}`; });
  signs.forEach(s => { s.style.transition = "opacity .35s ease"; });

  function frame(t) {
    // which leg, and how far along it
    let leg = 0, u = 0;
    for (let i = 0; i < 3; i++) {
      if (t >= legStart[i]) { leg = i; u = Math.min(1, (t - legStart[i]) / LEG[i]); }
    }
    if (t < legStart[0]) u = 0;
    const e = ease(u), d = stopLen[leg] + (stopLen[leg + 1] - stopLen[leg]) * e;
    [trail, glow].forEach(p => { p.style.strokeDashoffset = L - d; });
    const p = trail.getPointAtLength(d), q = trail.getPointAtLength(Math.min(L, d + 3)), r = trail.getPointAtLength(Math.max(0, d - 3));
    const ang = Math.atan2(q.y - r.y, q.x - r.x) * 180 / Math.PI;
    van.setAttribute("transform", `translate(${p.x.toFixed(1)} ${p.y.toFixed(1)})`);
    const flip = Math.abs(ang) > 90;
    vanBody.setAttribute("transform", flip ? `rotate(${ang - 180}) scale(-1 1)` : `rotate(${ang})`);
    // stops reached, signs shown
    const reached = i => i === 0 || d >= stopLen[i] - 0.5;
    stops.forEach((c, i) => { c.setAttribute("fill", reached(i) ? "#ff5a36" : "#fff"); c.setAttribute("stroke", reached(i) ? "#fff" : "#ff5a36"); });
    signs.forEach((s, i) => { s.style.opacity = reached(i) ? 1 : 0; });
    distEl.textContent = `${Math.round(km[leg] + (km[leg + 1] - km[leg]) * e)} km`;
    legEl.textContent = `${names[leg]}  →  ${names[leg + 1]}`;
    if (bar) bar.style.width = `${(t / TOTAL * 100).toFixed(2)}%`;
  }

  if (reduceMotion) { frame(legStart[2] + LEG[2] * 0.45); return; }
  let start = null, running = false, raf = 0;
  const loop = ts => {
    if (start === null) start = ts;
    frame(((ts - start) / 1000) % TOTAL);
    if (running) raf = requestAnimationFrame(loop);
  };
  // only animate while the hero is on screen
  new IntersectionObserver(([en]) => {
    running = en.isIntersecting;
    if (running) { start = null; raf = requestAnimationFrame(loop); } else cancelAnimationFrame(raf);
  }).observe(svg);
  frame(0);
})();

// ---- 2. Showreel --------------------------------------------------------------
(function showreel() {
  const chips = [...document.querySelectorAll(".chip[data-filter]")], reels = [...document.querySelectorAll(".reel")];
  chips.forEach(ch => ch.addEventListener("click", () => {
    const f = ch.dataset.filter;
    chips.forEach(c => c.setAttribute("aria-pressed", String(c === ch)));
    reels.forEach(r => { r.hidden = f !== "all" && !r.dataset.cat.split(" ").includes(f); });
  }));
  // a card with data-video="media/name.mp4" shows that video instead of the drawing
  reels.forEach(r => {
    const src = r.dataset.video;
    if (!src) return;
    const v = document.createElement("video");
    Object.assign(v, { muted: true, loop: true, playsInline: true, preload: "none" });
    v.setAttribute("aria-label", r.querySelector("h3")?.textContent || "Showreel video");
    v.src = src;
    r.querySelector(".reel-media svg")?.replaceWith(v);
  });
  // routes are drawn at rest; they animate in the first time a card is seen, and again on hover
  const replay = r => { if (reduceMotion) return; r.classList.remove("drawing"); void r.offsetWidth; r.classList.add("drawing"); };
  reels.forEach(r => r.addEventListener("mouseenter", () => replay(r)));
  const seen = new WeakSet();
  const io = new IntersectionObserver(entries => entries.forEach(en => {
    if (en.isIntersecting && !seen.has(en.target)) { seen.add(en.target); replay(en.target); }
    const v = en.target.querySelector("video");
    if (v && !reduceMotion) { if (en.isIntersecting) v.play().catch(() => {}); else v.pause(); }
  }), { threshold: 0.5 });
  reels.forEach(r => io.observe(r));
})();

// ---- 3. Forms -------------------------------------------------------------------
document.querySelectorAll(".js-form").forEach(form => {
  const status = form.querySelector(".form-status"), btn = form.querySelector("button[type=submit]");
  const say = (msg, kind) => { status.hidden = false; status.className = `form-status ${kind}`; status.textContent = msg; };
  form.addEventListener("submit", async e => {
    e.preventDefault();
    if (!form.checkValidity()) {
      const bad = form.querySelector(":invalid");
      say(bad && bad.type === "email" ? "Please enter a valid email address." : "Please fill in the required fields.", "err");
      bad?.focus();
      return;
    }
    const data = new FormData(form);
    if (data.get("_gotcha")) return; // a bot filled the hidden field
    data.delete("_gotcha");
    const subject = form.dataset.subject || "Website enquiry";
    if (!FORM_ENDPOINT) {
      // no form service yet: hand over to the visitor's email app
      const lines = [];
      for (const [k, v] of data.entries()) if (v && typeof v === "string") lines.push(`${k.replace(/_/g, " ")}: ${v}`);
      window.location.href = `mailto:${CONTACT_EMAIL}?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(lines.join("\n"))}`;
      say(`Your email app should open with the details filled in. If it doesn't, email ${CONTACT_EMAIL}.`, "ok");
      return;
    }
    data.append("_subject", subject);
    btn.disabled = true; const label = btn.textContent; btn.textContent = "Sending…";
    try {
      const res = await fetch(FORM_ENDPOINT, { method: "POST", body: data, headers: { Accept: "application/json" } });
      if (!res.ok) throw new Error(res.status);
      form.reset();
      say("Thanks. I’ll be in touch within one working day.", "ok");
    } catch {
      say(`That didn’t send. Please try again, or email ${CONTACT_EMAIL}.`, "err");
    } finally { btn.disabled = false; btn.textContent = label; }
  });
});
