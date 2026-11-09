/* Iterra Maps — client sample pages (for/<client>/index.html)
   Each client folder has an index.html with a window.SAMPLE settings block, plus its video and image files.
   This script builds the page from those settings, so improvements here reach every sample page at once. */
(function () {
  const S = Object.assign({
    company: "your company", firstName: "", tour: "your tour", intro: "", accent: "#0b7a75", logo: "", media: "",
    videos: [], offer: "", from: "Patrick", email: "hello@iterramaps.com",
    mode: "feedback",   // "feedback": ask for their opinion (no prices); "sale": show the offer and pricing
    note: "",         // feedback mode: text above the feedback button ("" = standard text)
  }, window.SAMPLE || {});
  S.note = S.note || "We’re getting Iterra Maps ready for the 2027 season and asking a few tour operators for honest feedback first. The video is yours to keep and use, whatever you think of it.";
  // what a finished video includes: sales wording only on "sale" pages
  S.includes = S.includes || (S.mode === "sale" ? [
    "Every stop on the itinerary, on the real roads, trails and sea crossings",
    "Your logo and route colours",
    "Widescreen, vertical and square versions, up to 4K",
    "One round of changes",
    "First version within 5 working days",
  ] : [
    "Every stop on the itinerary, on the real roads, trails and sea crossings",
    "Your logo and route colours",
    "Widescreen, vertical and square versions, up to 4K",
    "Stop names, and an elevation profile for hilly routes",
    "Your corrections, so the route matches the tour exactly",
  ]);

  const esc = s => String(s ?? "").replace(/[&<>"']/g, c => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
  const slug = s => String(s || "").toLowerCase().normalize("NFD").replace(/[̀-ͯ]/g, "").replace(/[^a-z0-9]+/g, "-").replace(/^-|-$/g, "");
  const ratio = a => { const [w, h] = String(a || "16:9").split(":").map(Number); return w > 0 && h > 0 ? w / h : 16 / 9; };
  const DL = '<svg width="16" height="16" viewBox="0 0 16 16" aria-hidden="true"><path d="M8 2v8m0 0L4.5 6.5M8 10l3.5-3.5M2.5 13.5h11" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg>';
  const MAIL = '<svg width="16" height="16" viewBox="0 0 16 16" aria-hidden="true"><path d="M2 3.5h12v9H2zM2.5 4l5.5 4.5L13.5 4" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round"/></svg>';
  const LOGO = '<svg width="34" height="34" viewBox="0 0 64 64" aria-hidden="true"><circle cx="32" cy="32" r="27" fill="none" stroke="#0e1b24" stroke-width="3"/><ellipse cx="32" cy="32" rx="12" ry="27" fill="none" stroke="#0e1b24" stroke-opacity=".28" stroke-width="2.5"/><path d="M5 32H59" stroke="#0e1b24" stroke-opacity=".28" stroke-width="2.5"/><path d="M11 46C22 50 30 30 38 28C46 26 46 18 50 14" fill="none" stroke="#ff5a36" stroke-width="5.5" stroke-linecap="round"/><circle cx="11" cy="46" r="4.5" fill="#0e1b24"/><circle cx="50" cy="14" r="5.5" fill="#fff" stroke="#0e1b24" stroke-width="3.5"/></svg>';

  // cookie choice and Google Analytics (does nothing until an ID is set in consent.js)
  if (!document.querySelector('script[src$="consent.js"]')) {
    const ck = document.createElement("script"); ck.src = "../../consent.js"; ck.defer = true; document.head.appendChild(ck);
  }

  document.documentElement.style.setProperty("--client", S.accent || "#0b7a75");

  const greeting = S.firstName ? `Hi ${esc(S.firstName)}, here’s ` : "Here’s ";
  const intro = S.intro ? esc(S.intro)
    : `We’ve turned ${esc(S.tour)} into a short animated route map, following your stops on the real roads and trails. Watch it below, download it, and share it with your team.`;
  const client = S.logo
    ? `<img class="sp-logo" src="${esc(S.logo)}" alt="${esc(S.company)}">`
    : `<strong class="sp-client-name">${esc(S.company)}</strong>`;

  const feedback = S.mode !== "sale";
  const subject = feedback ? `Feedback: ${S.tour} (${S.company})` : `Full reel: ${S.tour} (${S.company})`;
  const body = feedback ? `Hi ${S.from},\n\nThanks for the sample. Here's what we think:\n\n`
    : `Hi ${S.from},\n\nThanks for the sample. We'd like to talk about the full reel for ${S.tour}.\n\n`;
  const mailto = `mailto:${S.email}?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(body)}`;
  // feedback form on the main site, with this prospect's details filled in
  const formUrl = "../../feedback.html?" + new URLSearchParams({ company: S.company, tour: S.tour, page: location.href.split(/[?#]/)[0] });
  const cta = feedback ? `
        <h2>What do you think?</h2>
        <p>${esc(S.note)}</p>
        <div class="sp-buttons">
          <a class="btn btn-primary" href="${esc(formUrl)}">Give us your feedback <span class="sp-time">(2 minutes)</span></a>
          <a class="btn btn-outline" href="${esc(mailto)}">${MAIL}Reply by email</a>
        </div>` : `
        <h2>Like it?</h2>
        ${S.offer ? `<p>${esc(S.offer)}</p>` : ""}
        <div class="sp-buttons">
          <a class="btn btn-primary" href="${esc(mailto)}">${MAIL}Email us about the full reel</a>
          <a class="btn btn-outline" href="../../index.html#pricing">See pricing and FAQ</a>
        </div>`;

  // video files live on R2 (media.iterramaps.com); a plain file name is looked up in S.media
  const videoUrl = src => /^https?:\/\//.test(src) || !S.media ? src : S.media.replace(/\/?$/, "/") + src;
  let vi = 0; // one running number for every video on the page
  const videoList = list => (list || []).filter(v => v && v.src).map(v => Object.assign({}, v, { src: videoUrl(v.src) })).map(v => {
    const i = vi++;
    const r = ratio(v.aspect), tall = r < 1;
    const file = v.file || `${slug(S.company) || "iterra"}-${slug(S.tour) || "sample"}-${String(v.aspect || "16:9").replace(":", "x")}.mp4`;
    return `<figure class="sp-video${tall ? " tall" : ""}" style="--r:${r.toFixed(4)}">
      <div class="sp-frame" style="aspect-ratio:${r.toFixed(4)}">
        <video controls muted loop playsinline preload="metadata" data-autoplay${v.poster ? ` poster="${esc(v.poster)}"` : ""} src="${esc(v.src)}" aria-label="${esc(v.label || "Sample video")}"></video>
        <p class="sp-missing" hidden>This video is on its way.</p>
      </div>
      <figcaption><span>${esc(v.label || "")}</span>
        <a class="sp-dl" href="${esc(v.src)}" download="${esc(file)}" data-i="${i}">${DL}<span>Download MP4</span></a></figcaption>
    </figure>`;
  }).join("");
  const videos = videoList(S.videos);
  // optional second row, e.g. an extra clip: more: { title: "…", text: "…", videos: [ … ] }
  const moreVideos = S.more ? videoList(S.more.videos) : "";
  const more = moreVideos ? `
    <section class="sp-more-vids" aria-label="${esc(S.more.title || "More videos")}">
      ${S.more.title ? `<h2>${esc(S.more.title)}</h2>` : ""}${S.more.text ? `<p>${esc(S.more.text)}</p>` : ""}
      <div class="sp-videos">${moreVideos}</div>
    </section>` : "";

  document.getElementById("sample-page").innerHTML = `
  <div class="sp-stripe" aria-hidden="true"></div>
  <header class="site-header">
    <div class="wrap">
      <a class="brand" href="../../" aria-label="Iterra Maps home">${LOGO}<span class="brand-name">Iterra <span>Maps</span></span></a>
      <p class="sp-for"><span>Sample made for</span> ${client}</p>
    </div>
  </header>
  <main id="main" class="wrap sp">
    <section class="sp-hero">
      <p class="eyebrow">Free sample</p>
      <h1>${greeting}<em>${esc(S.tour)}</em> in motion.</h1>
      <p class="lead">${intro}</p>
    </section>

    <section class="sp-videos" aria-label="Sample videos">${videos || '<p class="small">Videos coming soon.</p>'}</section>${more}

    <section class="sp-next">
      <div class="sp-includes">
        <h2>${feedback ? "What a finished version would include" : "What the full reel includes"}</h2>
        <ul>${S.includes.map(x => `<li>${esc(x)}</li>`).join("")}</ul>
      </div>
      <div class="sp-cta">${cta}
        <p class="sp-sign">— ${esc(S.from)} at Iterra Maps · <a href="mailto:${esc(S.email)}">${esc(S.email)}</a></p>
      </div>
    </section>

    <p class="small sp-private">This page was made for ${esc(S.company)}. It isn’t listed on the site or in search engines, so only people you share the link with will find it. You’re welcome to share the sample with your team.</p>
  </main>
  <footer class="site-footer">
    <div class="wrap">
      <div class="cols"><span class="brand-name">Iterra <span>Maps</span></span><span>Animated route maps</span><a href="mailto:${esc(S.email)}">${esc(S.email)}</a></div>
      <div class="cols"><a href="../../privacy.html">Privacy notice</a><a href="#" class="js-cookie-settings">Cookie settings</a><span>Map data in videos © OpenStreetMap contributors</span><span>© ${new Date().getFullYear()} Iterra Maps</span></div>
    </div>
  </footer>`;

  // logo that fails to load: show the name instead
  const logo = document.querySelector(".sp-logo");
  logo?.addEventListener("error", () => { logo.outerHTML = `<strong class="sp-client-name">${esc(S.company)}</strong>`; });

  // missing video: say so, and hide its download link
  document.querySelectorAll(".sp-video").forEach(fig => {
    const v = fig.querySelector("video");
    v.addEventListener("error", () => {
      v.hidden = true; fig.querySelector(".sp-missing").hidden = false; fig.querySelector(".sp-dl").hidden = true;
      console.warn(`Sample page: couldn't load ${v.getAttribute("src")}`);
    });
    // only one video plays at a time
    v.addEventListener("play", () => document.querySelectorAll(".sp-video video").forEach(o => { if (o !== v && !o.paused) { o._ours = true; o.pause(); } }));
    // Google Analytics event (only sent if the visitor accepted analytics cookies): which prospect watched which video.
    // A video starting by itself doesn't count; the visitor pressing play, unmuting or going full screen does.
    let played = false;
    const watched = how => {
      if (played || typeof window.gtag !== "function") return; played = true;
      window.gtag("event", "sample_video_play", { company: S.company, tour: S.tour, video: v.getAttribute("src") || "", how });
    };
    v.addEventListener("play", () => { if (!v._ours) watched("play"); });
    v.addEventListener("volumechange", () => { if (!v.muted && v.volume > 0) watched("unmute"); });
    v.addEventListener("fullscreenchange", () => { if (document.fullscreenElement === v) watched("fullscreen"); });
    v.addEventListener("webkitbeginfullscreen", () => watched("fullscreen"));
  });

  // The videos play by themselves, silently, while on screen (one at a time; not with reduced motion or data saver on).
  // A video the visitor pauses stays paused.
  (function autoplay() {
    const vids = [...document.querySelectorAll(".sp-video video[data-autoplay]")];
    if (!vids.length || !("IntersectionObserver" in window)) return;
    if (matchMedia("(prefers-reduced-motion: reduce)").matches || navigator.connection?.saveData) return;
    const io = new IntersectionObserver(es => es.forEach(e => {
      const v = e.target;
      if (e.isIntersecting && e.intersectionRatio >= 0.25) { if (v.paused && !v._userPaused && !vids.some(o => o !== v && !o.paused)) start(v); } // never takes over from a video already playing
      else if (!e.isIntersecting && !v.paused) { v._ours = true; v.pause(); } // off screen: pause
    }), { threshold: [0, 0.25, 0.5] });
    const start = v => { v._ours = true; v.muted = true; v.play().catch(() => { v._ours = false; }); };
    vids.forEach(v => {
      v.addEventListener("pause", () => { if (v._ours) v._ours = false; else if (!v.ended) v._userPaused = true; });
      v.addEventListener("play", () => setTimeout(() => { v._ours = false; v._userPaused = false; }, 0)); // after the play listeners above have looked
      io.observe(v);
    });
  })();

  // Download buttons: browsers ignore "download" on links to another address (the videos are on media.iterramaps.com),
  // so fetch the file and save it from here instead. If that fails, open the video in a new tab.
  document.querySelectorAll(".sp-dl").forEach(a => a.addEventListener("click", () => {
    if (typeof window.gtag === "function") window.gtag("event", "sample_video_download", { company: S.company, tour: S.tour, video: a.getAttribute("href") || "" });
  }));
  document.querySelectorAll(".sp-dl").forEach(a => a.addEventListener("click", async e => {
    if (new URL(a.href, location.href).origin === location.origin) return;
    e.preventDefault();
    const label = a.querySelector("span"), was = label.textContent;
    label.textContent = "Downloading…";
    try {
      const r = await fetch(a.href, { mode: "cors" });
      if (!r.ok) throw new Error(r.status);
      const url = URL.createObjectURL(await r.blob());
      const tmp = Object.assign(document.createElement("a"), { href: url, download: a.getAttribute("download") });
      document.body.append(tmp); tmp.click(); tmp.remove();
      setTimeout(() => URL.revokeObjectURL(url), 60000);
    } catch { window.open(a.href, "_blank", "noopener"); }
    label.textContent = was;
  }));

  // file sizes on the download buttons
  document.querySelectorAll(".sp-dl").forEach(a => {
    fetch(a.href, { method: "HEAD" }).then(r => {
      const n = +r.headers.get("content-length");
      if (r.ok && n) a.querySelector("span").textContent = `Download MP4 (${(n / 1048576).toFixed(1)} MB)`;
    }).catch(() => {});
  });

  document.title = document.title || `A sample for ${S.company} · Iterra Maps`;
})();
