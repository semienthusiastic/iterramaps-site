/* Iterra Maps — site script
   1. Hero: a looping mini version of the product (route draws, van drives, signs pop up, distance counts).
   2. Showreel: filters. Each card shows its image with a play button; on a computer, the mouse resting on a card
      plays the video silently in the card (nothing plays by itself); clicking or tapping opens it full size in a pop-up.
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
// Each card: <img> (shown at rest) + data-video="media/name.mp4". Optional: data-aspect="9:16" for vertical videos.
// If a card's image is missing, a frame of its video is shown instead: data-thumb="12" picks the second
// (default: just before the end, with the whole route drawn).
(function showreel() {
  const chips = [...document.querySelectorAll(".chip[data-filter]")], reels = [...document.querySelectorAll(".reel")];
  chips.forEach(ch => ch.addEventListener("click", () => {
    const f = ch.dataset.filter;
    chips.forEach(c => c.setAttribute("aria-pressed", String(c === ch)));
    reels.forEach(r => { r.hidden = f !== "all" && !r.dataset.cat.split(" ").includes(f); });
  }));

  const canHover = window.matchMedia("(hover: hover) and (pointer: fine)").matches;
  const hoverPlay = canHover && !reduceMotion;
  const saveData = navigator.connection?.saveData;
  const PLAY = '<svg viewBox="0 0 14 14" aria-hidden="true"><path d="M3 1.5L12 7 3 12.5z" fill="currentColor"/></svg>';
  const hint = document.querySelector(".js-reel-hint");
  if (hint && !hoverPlay) hint.textContent = canHover ? "Click a reel to watch it full size." : "Tap a reel to watch it full size.";

  // ---- the pop-up player
  const dlg = document.getElementById("reel-player");
  const dv = dlg?.querySelector("video"), dTitle = dlg?.querySelector("#reel-player-title");
  let opener = null;
  function openPlayer(r) {
    if (r.classList.contains("video-missing")) return;
    const src = r.dataset.video, title = r.querySelector("h3")?.textContent || "Showreel";
    stopPreview(r);
    if (!dlg || typeof dlg.showModal !== "function") { window.open(src, "_blank", "noopener"); return; }
    const [aw, ah] = (r.dataset.aspect || "16:9").split(":").map(Number);
    dlg.classList.toggle("vertical", ah > aw);
    dlg.style.setProperty("--ar", `${aw} / ${ah}`);
    dlg.style.setProperty("--arw", String(aw / ah));
    dTitle.textContent = title;
    dv.setAttribute("aria-label", title);
    const img = r.querySelector(".reel-media img");
    if (img && !r.classList.contains("no-image") && ah <= aw) dv.poster = img.currentSrc || img.src; else dv.removeAttribute("poster");
    dv.src = src;
    opener = r.querySelector(".reel-open");
    dlg.showModal();
    dv.play().catch(() => {}); // the visitor clicked play, so playback with sound is allowed
  }
  if (dlg) {
    dlg.querySelector(".reel-player-close").addEventListener("click", () => dlg.close());
    dlg.addEventListener("click", e => { if (e.target === dlg) dlg.close(); }); // click on the dark backdrop
    dlg.addEventListener("close", () => {
      dv.pause(); dv.removeAttribute("src"); dv.load(); // stop downloading
      opener?.focus(); opener = null;
    });
  }

  // ---- fallback still (only used when a card's image is missing)
  const thumbTime = r => {
    if (r.dataset.thumb) return Math.max(0, parseFloat(r.dataset.thumb) || 0);
    const v = r._video, len = (r.querySelector(".reel-len")?.textContent || "").split(":").map(Number);
    const d = v && isFinite(v.duration) ? v.duration : len.length === 2 ? len[0] * 60 + len[1] : 0;
    return Math.max(0, d - 0.6);
  };
  const showStill = r => { const v = r._video; if (v.readyState >= 1) { try { v.currentTime = Math.min(thumbTime(r), v.duration - 0.05); } catch {} } };

  function load(r) {
    const v = r._video;
    if (v.getAttribute("src")) return;
    // with no image, the #t= part makes phones (iOS Safari in particular) show that frame instead of a blank box
    v.src = r.classList.contains("no-image") ? `${r.dataset.video}#t=${thumbTime(r).toFixed(1)}` : r.dataset.video;
  }

  // ---- hover preview: muted, from the start, looping while the pointer stays on the card
  function startPreview(r) {
    const v = r._video;
    if (!v || r.classList.contains("video-missing")) return;
    r.classList.add("previewing");
    load(r);
    try { v.currentTime = 0; } catch {}
    v.play().catch(() => {});
  }
  function stopPreview(r) {
    const v = r._video;
    r.classList.remove("previewing", "video-on");
    if (!v) return;
    v.pause();
    if (r.classList.contains("no-image")) showStill(r);
    else setTimeout(() => { if (!r.classList.contains("previewing")) { try { v.currentTime = 0; } catch {} } }, 320); // after the fade
  }

  function noImage(r) {
    if (r.classList.contains("no-image")) return;
    r.classList.add("no-image");
    const v = r._video;
    if (!v) return;
    v.preload = hoverPlay && !saveData ? "auto" : "metadata";
    if (r._seen) load(r);
  }

  reels.forEach(r => {
    if (!r.dataset.video) return;
    r.classList.add("has-video");
    const media = r.querySelector(".reel-media"), title = r.querySelector("h3")?.textContent || "showreel";
    const v = document.createElement("video");
    Object.assign(v, { muted: true, loop: true, playsInline: true, preload: "none", tabIndex: -1, disablePictureInPicture: true });
    v.setAttribute("muted", ""); v.setAttribute("aria-hidden", "true");
    v.addEventListener("playing", () => { if (r.classList.contains("previewing")) r.classList.add("video-on"); });
    v.addEventListener("loadedmetadata", () => {
      if (!r.classList.contains("no-image") || r.classList.contains("previewing")) return;
      showStill(r);
      // Phones (Android Chrome especially) don't paint a frame until the video has played: play it silently for a
      // moment, then put it back on the still.
      if (!hoverPlay) {
        const back = () => { v.removeEventListener("timeupdate", back); v.pause(); showStill(r); };
        v.addEventListener("timeupdate", back);
        v.play().catch(() => v.removeEventListener("timeupdate", back));
      }
    });
    v.addEventListener("error", () => { // file not uploaded yet (or misnamed): no play button on this card
      r.classList.add("video-missing"); r.classList.remove("has-video", "previewing", "video-on");
      media.querySelector(".reel-open")?.remove(); media.querySelector(".reel-hover")?.remove();
      console.warn(`Showreel: couldn't load ${r.dataset.video}`);
    });
    r._video = v;
    const img = media.querySelector("img");
    if (img) img.after(v); else media.prepend(v);

    if (hoverPlay) media.insertAdjacentHTML("beforeend", '<span class="reel-hover" aria-hidden="true">Click to watch</span>');
    const btn = document.createElement("button");
    btn.type = "button"; btn.className = "reel-open";
    btn.setAttribute("aria-label", `Play video: ${title}`);
    btn.innerHTML = `<span class="reel-play">${PLAY}</span>`;
    btn.addEventListener("click", () => openPlayer(r));
    media.append(btn);
    r.querySelector(".reel-body").addEventListener("click", () => openPlayer(r));
    if (hoverPlay) {
      r.addEventListener("mouseenter", () => startPreview(r));
      r.addEventListener("mouseleave", () => stopPreview(r));
    }

    // a missing image falls back to a frame of the video
    if (!img) noImage(r);
    else {
      img.addEventListener("error", () => { console.warn(`Showreel: couldn't load ${img.getAttribute("src")}; showing a frame of the video instead`); noImage(r); });
      // an image that already failed before this script ran: confirm with a fresh request, so a lazy image that
      // simply hasn't loaded yet is never mistaken for a missing one
      if (img.complete && img.naturalWidth === 0 && img.getAttribute("src")) {
        const probe = new Image();
        probe.onerror = () => noImage(r);
        probe.src = img.src;
      }
    }
  });

  // shortly before a card scrolls into view: on a computer, let the browser start buffering its video so the hover
  // preview starts at once (not on data saver). Phones load only the image, and the video when it's tapped.
  const io = new IntersectionObserver(entries => entries.forEach(en => {
    const r = en.target;
    if (!en.isIntersecting || !r._video) return;
    r._seen = true; io.unobserve(r);
    if (hoverPlay && !saveData) { r._video.preload = "auto"; load(r); }
    else if (r.classList.contains("no-image")) load(r);
  }), { rootMargin: "400px 0px" });
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
      window.location.href = "thanks.html";
    } catch {
      say(`That didn’t send. Please try again, or email ${CONTACT_EMAIL}.`, "err");
    } finally { btn.disabled = false; btn.textContent = label; }
  });
});
