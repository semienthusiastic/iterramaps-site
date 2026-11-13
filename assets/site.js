/* Iterra Maps — site script. One file for every public page.
   1. Prices in dollars or euro   2. Header menu   3. The video player   4. "Jump to" buttons
   5. The journey line on audience and showcase pages   6. Showcase filters   7. Forms */
(() => {
"use strict";
const FORM_ENDPOINT = "https://formspree.io/f/xyekdlbg";   // Formspree; leave "" to open the visitor's email app instead
const CONTACT_EMAIL = "hello@iterramaps.com";
const $ = (s, r = document) => r.querySelector(s), $$ = (s, r = document) => [...r.querySelectorAll(s)];
const reduceMotion = matchMedia("(prefers-reduced-motion: reduce)").matches;
const saveData = !!(navigator.connection && navigator.connection.saveData);
$$(".js-year").forEach(el => { el.textContent = new Date().getFullYear(); });

// ---- 1. Prices: pages are written in dollars; visitors in a European time zone see euro; the switch overrides it
(function currency() {
  const KEY = "iterra.currency";
  const detect = () => {
    try { const v = localStorage.getItem(KEY); if (v === "usd" || v === "eur") return v; } catch (e) {}
    let tz = ""; try { tz = Intl.DateTimeFormat().resolvedOptions().timeZone || ""; } catch (e) {}
    return /^Europe\//.test(tz) || /^Atlantic\/(Azores|Madeira|Canary|Faroe|Reykjavik)$/.test(tz) ? "eur" : "usd";
  };
  const apply = cur => {
    document.documentElement.dataset.currency = cur;
    $$("[data-usd][data-eur]").forEach(el => { const v = el.getAttribute("data-" + cur); if (el.tagName === "INPUT") el.value = v; else el.textContent = v; });
    $$(".js-cur").forEach(b => b.setAttribute("aria-pressed", String(b.dataset.cur === cur)));
  };
  if (!$("[data-usd]")) return;
  apply(detect());
  document.addEventListener("click", e => { const b = e.target.closest(".js-cur"); if (!b) return; try { localStorage.setItem(KEY, b.dataset.cur); } catch (err) {} apply(b.dataset.cur); });
})();

// ---- 2. Header: the phone menu and the "Who it's for" menu
(function header() {
  const btn = $(".hd-toggle"), panel = $("#hd-panel");
  if (btn && panel) {
    const isOpen = () => btn.getAttribute("aria-expanded") === "true";
    const set = open => { btn.setAttribute("aria-expanded", String(open)); btn.setAttribute("aria-label", open ? "Close menu" : "Open menu"); panel.hidden = !open; document.body.classList.toggle("menu-open", open); };
    btn.addEventListener("click", () => set(!isOpen()));
    panel.addEventListener("click", e => { if (e.target.closest("a")) set(false); });
    document.addEventListener("keydown", e => { if (e.key === "Escape" && isOpen()) { set(false); btn.focus(); } });
    document.addEventListener("click", e => { if (isOpen() && !e.target.closest(".hd")) set(false); });
    matchMedia("(min-width: 960px)").addEventListener("change", e => { if (e.matches) set(false); });
  }
  const dd = $(".hd-dd-btn"), ddp = $("#hd-who");
  if (dd && ddp) {
    const set = open => { dd.setAttribute("aria-expanded", String(open)); ddp.hidden = !open; };
    dd.addEventListener("click", () => set(ddp.hidden));
    document.addEventListener("click", e => { if (!ddp.hidden && !e.target.closest(".hd-dd")) set(false); });
    document.addEventListener("keydown", e => { if (e.key === "Escape" && !ddp.hidden) { set(false); dd.focus(); } });
    ddp.addEventListener("focusout", e => { if (!e.relatedTarget || !e.relatedTarget.closest(".hd-dd")) set(false); });
  }
})();

// ---- 3. The video player: every <video> in the page gets the same controls.
// A video loads when it is about to scroll into view. Those marked data-autoplay play silently while on screen
// (not with reduced motion or data saver); a video the visitor pauses stays paused. Full screen opens the pop-up.
const fmt = s => `${Math.floor(s / 60)}:${String(Math.floor(s % 60)).padStart(2, "0")}`;
const ICON = {
  play: '<svg viewBox="0 0 16 16" aria-hidden="true"><path class="i-pause" d="M4 2.5h2.6v11H4zM9.4 2.5H12v11H9.4z" fill="currentColor"/><path class="i-play" d="M4.5 2.2L14 8l-9.5 5.8z" fill="currentColor"/></svg>',
  full: '<svg viewBox="0 0 16 16" aria-hidden="true"><path d="M2 6V2h4M10 2h4v4M14 10v4h-4M6 14H2v-4" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/></svg>',
};
const dlg = $("#reel-player"), dv = dlg && $("video", dlg);
let dlgOpener = null;
function openVideo(src, aspect, title, poster, opener, at) {
  if (!dlg || typeof dlg.showModal !== "function") { window.open(src, "_blank", "noopener"); return; }
  const [aw, ah] = (aspect || "16:9").split(":").map(Number);
  dlg.classList.toggle("vertical", ah > aw);
  dlg.style.setProperty("--ar", `${aw} / ${ah}`); dlg.style.setProperty("--arw", String(aw / ah));
  $("#reel-player-title", dlg).textContent = title || "Video";
  dv.setAttribute("aria-label", title || "Video");
  if (poster) dv.poster = poster; else dv.removeAttribute("poster");
  dv.src = src; dlgOpener = opener || null;
  dlg.showModal();
  if (at) dv.addEventListener("loadedmetadata", () => { try { dv.currentTime = at; } catch (e) {} }, { once: true });
  dv.play().catch(() => {});
}
if (dlg) {
  $(".reel-player-close", dlg).addEventListener("click", () => dlg.close());
  dlg.addEventListener("click", e => { if (e.target === dlg) dlg.close(); });
  dlg.addEventListener("close", () => { dv.pause(); dv.removeAttribute("src"); dv.load(); if (dlgOpener) dlgOpener.focus(); dlgOpener = null; });
}
const players = [];
(function videoPlayers() {
  const vids = $$("main video");
  if (!vids.length) return;
  const auto = !reduceMotion && !saveData;
  const srcOf = v => (v.dataset.src || v.getAttribute("src") || "").split("#")[0];
  const load = v => {
    if (v._loaded) return; v._loaded = true;
    const src = srcOf(v), thumb = v.dataset.thumb;
    // with no poster image, #t= makes phones show a frame from the route instead of an empty box
    v.src = src + (!v.getAttribute("poster") && thumb ? `#t=${thumb}` : "");
  };
  vids.forEach(v => {
    let box = v.parentElement;
    if (!box.classList.contains("vp")) {
      box = document.createElement("div");
      const shape = v.closest(".rt-shape-tall, .sc-phone") ? "tall" : v.closest(".rt-shape-sq") ? "sq" : "wide";
      box.className = `vp vp-${shape}`;
      v.before(box); box.append(v);
    }
    const aspect = box.classList.contains("vp-tall") ? "9:16" : box.classList.contains("vp-sq") ? "1:1" : "16:9";
    if (aspect !== "16:9" || box.clientWidth < 420) box.classList.add("vp-small");
    const title = v.getAttribute("aria-label") || "Video";
    // an existing src (older pages) becomes a lazy one, so nothing downloads until it is needed
    if (v.getAttribute("src")) { v.dataset.src = srcOf(v); const t = (v.getAttribute("src").split("#t=")[1] || ""); if (t && !v.dataset.thumb) v.dataset.thumb = t; v.removeAttribute("src"); v.load(); }
    v.removeAttribute("controls"); v.preload = "none"; v.muted = true; v.playsInline = true;
    const ui = document.createElement("div"); ui.className = "vp-ui";
    ui.innerHTML = `<button type="button" class="vp-btn vp-toggle" aria-label="Play video: ${title.replace(/"/g, "&quot;")}">${ICON.play}</button><div class="vp-bar" aria-hidden="true"><i></i></div><span class="vp-time" aria-hidden="true">0:00</span><button type="button" class="vp-btn vp-full" aria-label="Full screen">${ICON.full}</button>`;
    box.append(ui);
    const tg = $(".vp-toggle", ui), bar = $(".vp-bar i", ui), time = $(".vp-time", ui);
    const toggle = () => { load(v); if (v.paused) { v._held = false; v.play().catch(() => {}); } else { v._held = true; v.pause(); } };
    tg.addEventListener("click", toggle);
    v.addEventListener("click", toggle);
    v.addEventListener("play", () => { if (!v._counted && !v._auto && typeof window.gtag === "function") { v._counted = true; window.gtag("event", "video_play", { video: srcOf(v).split("/").slice(-2).join("/") }); } }, { once: false });
    v.addEventListener("play", () => { box.classList.add("is-playing"); tg.setAttribute("aria-label", `Pause video: ${title}`); });
    v.addEventListener("pause", () => { box.classList.remove("is-playing"); tg.setAttribute("aria-label", `Play video: ${title}`); });
    v.addEventListener("timeupdate", () => { if (v.duration) bar.style.width = `${(v.currentTime / v.duration * 100).toFixed(2)}%`; time.textContent = fmt(v.currentTime); });
    v.addEventListener("error", () => {
      if (!v._loaded) return;
      // a small web copy that isn't on R2 yet: play the full-size original instead
      const cur = srcOf(v);
      if (/\.web\.mp4$/.test(cur)) { v.dataset.src = cur.replace(/\.web\.mp4$/, ".mp4"); v._loaded = false; const play = !v.paused || v._auto; load(v); if (play) v.play().catch(() => {}); return; }
      const shape = v.closest(".rt-shape"); if (shape) { shape.remove(); return; }   // a missing extra shape closes up
      box.classList.add(v.getAttribute("poster") ? "vp-novideo" : "vp-missing"); console.warn(`Video: couldn't load ${srcOf(v)}`);
    }, true);
    $(".vp-full", ui).addEventListener("click", e => { const at = v.currentTime || 0; v._held = true; v.pause(); openVideo(srcOf(v), aspect, title, v.getAttribute("poster") || "", e.currentTarget, at); });
    v._auto = auto && v.hasAttribute("data-autoplay");
    players.push({ v, load });
  });
  if (!("IntersectionObserver" in window)) { vids.forEach(load); return; }
  const near = new IntersectionObserver(es => es.forEach(en => { if (en.isIntersecting) { near.unobserve(en.target); if (en.target._auto || !en.target.getAttribute("poster")) load(en.target); } }), { rootMargin: "400px 0px" });
  const onScreen = new IntersectionObserver(es => es.forEach(en => {
    const v = en.target;
    if (en.isIntersecting && en.intersectionRatio >= 0.35) { if (v._auto && !v._held && !(dlg && dlg.open)) { load(v); v.play().catch(() => {}); } }
    else if (!en.isIntersecting && !v.paused) v.pause();
  }), { threshold: [0, 0.35] });
  vids.forEach(v => { near.observe(v); onScreen.observe(v); });
})();
// cards that open a short film in the pop-up (showcase index)
$$("[data-open-video]").forEach(b => b.addEventListener("click", () => openVideo(b.dataset.openVideo, b.dataset.aspect, b.dataset.title, b.dataset.poster || "", b)));
// a GIF that isn't uploaded yet: drop its tile so the row closes up
$$(".pg-gif img").forEach(i => { const drop = () => { const r = i.closest(".rt-shapes"); if (r) r.classList.remove("pg-shapes4"); i.closest(".pg-gif").remove(); }; i.addEventListener("error", drop); if (i.complete && i.naturalWidth === 0 && i.getAttribute("src") && i.loading !== "lazy") drop(); });
// "Play all four from the start" on the looks page
const sync = $(".pg-lv-sync");
if (sync) sync.addEventListener("click", () => {
  const ps = players.filter(p => p.v.closest(".pg-lv")); ps.forEach(p => { p.load(p.v); p.v.pause(); p.v._held = false; });
  Promise.all(ps.map(p => new Promise(r => p.v.readyState >= 3 ? r() : p.v.addEventListener("canplay", r, { once: true })))).then(() => ps.forEach(p => { try { p.v.currentTime = 0; } catch (e) {} p.v.play().catch(() => {}); }));
});

// ---- 4. "Jump to" buttons: play the page's main video from that moment
$$("[data-at]").forEach(b => b.addEventListener("click", () => {
  const p = players.find(x => x.v.hasAttribute("data-main")) || players[0]; if (!p) return;
  const v = p.v, at = +b.dataset.at; p.load(v); v._held = false;
  const go = () => { try { v.currentTime = at; } catch (e) {} v.play().catch(() => {}); };
  if (v.readyState >= 1) go(); else v.addEventListener("loadedmetadata", go, { once: true });
  v.closest(".vp").scrollIntoView({ behavior: reduceMotion ? "auto" : "smooth", block: "center" });
}));

// ---- 5. The journey line fills in as you read, like the route in the videos
(function journey() {
  const j = $(".pg-journey"); if (!j) return;
  const marks = $$(".pg-stop > .pg-stop-mark, .pg-dest > .pg-stop-mark", j), last = marks[marks.length - 1];
  if (!last) return;
  j.classList.add("is-live");
  let raf = 0;
  const update = () => { raf = 0;
    const r = j.getBoundingClientRect(), lr = last.getBoundingClientRect(), line = innerHeight * .62;
    const end = r.bottom - (lr.top + lr.height / 2); j.style.setProperty("--end", end.toFixed(1) + "px");
    const atBottom = scrollY + innerHeight >= document.documentElement.scrollHeight - 4;
    const p = atBottom ? 1 : (line - r.top - 10) / (r.height - 10 - end);
    j.style.setProperty("--p", Math.max(0, Math.min(1, p)).toFixed(4));
    marks.forEach(m => { const b = m.getBoundingClientRect(); m.parentElement.classList.toggle("is-reached", atBottom || b.top + b.height / 2 <= line); }); };
  addEventListener("scroll", () => { if (!raf) raf = requestAnimationFrame(update); }, { passive: true });
  addEventListener("resize", update); update();
})();

// ---- 6. Showcase filters: the buttons hide cards; without this script every card shows
(function filters() {
  const chips = $$(".chip[data-filter]"); if (!chips.length) return;
  const cards = $$("[data-kind]"), status = $(".filter-status");
  chips.forEach(ch => ch.addEventListener("click", () => {
    const f = ch.dataset.filter; let n = 0;
    chips.forEach(c => c.setAttribute("aria-pressed", String(c === ch)));
    cards.forEach(c => { const show = f === "all" || c.dataset.kind.split(" ").includes(f); c.hidden = !show; if (show) n++; });
    if (status) status.textContent = `${n} ${n === 1 ? "film" : "films"} shown`;
  }));
})();

// ---- 7. Forms: check the fields, show each problem beside its field, send to Formspree
$$(".js-form").forEach(form => {
  const status = $(".form-status", form), btn = $("button[type=submit]", form);
  const say = (msg, kind) => { status.hidden = false; status.className = `form-status ${kind}`; status.textContent = msg; };
  const params = new URLSearchParams(location.search);
  $$("input[type=text][name], input[type=hidden][name]", form).forEach(f => { const v = params.get(f.name); if (v && !f.value) f.value = v.slice(0, 300); });
  const from = (document.referrer.match(/\/made-for\/([a-z-]+)\//) || [])[1];   // which audience page sent them
  if (from) { const h = $("input[name=from_page]", form); if (h) h.value = from; }
  const mark = (f, msg) => {
    const id = f.id + "-err"; let m = document.getElementById(id);
    if (!msg) { f.removeAttribute("aria-invalid"); f.removeAttribute("aria-describedby"); if (m) m.remove(); return; }
    if (!m) { m = document.createElement("span"); m.id = id; m.className = "field-err"; f.after(m); }
    m.textContent = msg; f.setAttribute("aria-invalid", "true"); f.setAttribute("aria-describedby", id);
  };
  const problem = f => {
    if (f.validity.valueMissing) return f.dataset.missing || "Please fill this in.";
    if (f.validity.typeMismatch && f.type === "email") return "Please enter a valid email address, like you@yourcompany.com.";
    if (f.validity.typeMismatch && f.type === "url") return "Please enter a full link, starting with https://";
    return f.validity.valid ? "" : "Please check this field.";
  };
  const fields = $$("input[required], textarea[required], input[type=email], input[type=url]", form);
  fields.forEach(f => f.addEventListener("input", () => { if (f.getAttribute("aria-invalid")) mark(f, problem(f)); }));
  form.addEventListener("submit", async e => {
    e.preventDefault();
    const bad = fields.filter(f => { const p = problem(f); mark(f, p); return p; });
    if (bad.length) { status.hidden = true; bad[0].focus(); return; }
    const data = new FormData(form);
    if (data.get("_gotcha")) return;   // a bot filled the hidden field
    data.delete("_gotcha");
    const who = (data.get("company") || "").trim();
    const subject = (form.dataset.subject || "Website inquiry") + (who ? `: ${who}` : "");
    if (!FORM_ENDPOINT) {
      const lines = []; for (const [k, v] of data.entries()) if (v && typeof v === "string") lines.push(`${k.replace(/_/g, " ")}: ${v}`);
      location.href = `mailto:${CONTACT_EMAIL}?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(lines.join("\n"))}`;
      say(`Your email app should open with the details filled in. If it doesn't, email ${CONTACT_EMAIL}.`, "ok"); return;
    }
    data.append("_subject", subject);
    btn.disabled = true; const label = btn.textContent; btn.textContent = "Sending…";
    try {
      const res = await fetch(FORM_ENDPOINT, { method: "POST", body: data, headers: { Accept: "application/json" } });
      if (!res.ok) throw new Error(res.status);
      if (typeof window.gtag === "function") window.gtag("event", "form_sent", { form: form.dataset.subject || "" });
      form.reset();
      const done = form.dataset.done ? document.getElementById(form.dataset.done) : null;
      if (done) { form.hidden = true; done.hidden = false; done.scrollIntoView({ block: "start" }); if (done.focus) done.focus(); }
      else location.href = "/thanks.html";
    } catch (err) { say(`That didn’t send. Please try again, or email ${CONTACT_EMAIL}.`, "err"); }
    finally { btn.disabled = false; btn.textContent = label; }
  });
});
// clicks on the main call to action, for visitors who accepted analytics
document.addEventListener("click", e => { const a = e.target.closest("a[href$='/sample.html'], a[href^='mailto:']"); if (a && typeof window.gtag === "function") window.gtag("event", "cta_click", { to: a.getAttribute("href").slice(0, 60), text: (a.textContent || "").trim().slice(0, 60) }); });
})();
