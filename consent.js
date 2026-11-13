/* Iterra Maps — Google Analytics, only with the visitor's permission.
   A slim bar along the bottom asks once; analytics stays off until Accept. The choice is kept in this browser
   for 12 months, then we ask again. Private sample pages (/for/…) and the embed player load no analytics
   and show no bar. */
(function () {
  const GA_ID = "G-GKXKNKSLET";
  const KEY = "iterra.consent";
  const MAX_AGE = 365 * 24 * 3600 * 1000;
  const enabled = /^G-[A-Z0-9]{6,}$/.test(GA_ID) && !/^G-X+$/.test(GA_ID) && !/^\/(for|embed)\//.test(location.pathname);

  function ready(fn) { document.readyState === "loading" ? document.addEventListener("DOMContentLoaded", fn) : fn(); }
  if (!enabled) {
    ready(() => document.querySelectorAll(".js-cookie-settings").forEach(el => (el.closest("li") || el).remove()));
    return;
  }
  function read() {
    try { const v = JSON.parse(localStorage.getItem(KEY) || "null"); return v && (v.c === "granted" || v.c === "denied") && Date.now() - v.t < MAX_AGE ? v.c : null; }
    catch (e) { return null; }
  }
  function save(c) { try { localStorage.setItem(KEY, JSON.stringify({ c, t: Date.now() })); } catch (e) {} }

  // Consent Mode v2: everything denied until the visitor says yes
  window.dataLayer = window.dataLayer || [];
  window.gtag = function () { dataLayer.push(arguments); };
  gtag("consent", "default", { analytics_storage: "denied", ad_storage: "denied", ad_user_data: "denied", ad_personalization: "denied" });

  let loaded = false;
  function startAnalytics() {
    gtag("consent", "update", { analytics_storage: "granted" });
    if (loaded) return;
    loaded = true;
    const s = document.createElement("script"); s.async = true; s.src = "https://www.googletagmanager.com/gtag/js?id=" + GA_ID;
    document.head.appendChild(s);
    gtag("js", new Date());
    gtag("config", GA_ID, { anonymize_ip: true });
  }
  function clearCookies() {
    const host = location.hostname.replace(/^www\./, "");
    document.cookie.split(";").map(c => c.split("=")[0].trim()).filter(n => /^_ga/.test(n)).forEach(n => {
      [host, "." + host, location.hostname].forEach(d => { document.cookie = `${n}=; expires=Thu, 01 Jan 1970 00:00:00 GMT; path=/; domain=${d}`; });
      document.cookie = `${n}=; expires=Thu, 01 Jan 1970 00:00:00 GMT; path=/`;
    });
  }

  const css = `
  .ck{position:fixed;z-index:100;left:0;right:0;bottom:0;background:#0e1b24;color:#dfe6ea;border-top:1px solid rgba(255,255,255,.16);
      box-shadow:0 -6px 24px rgba(0,0,0,.18);font:400 14px/1.45 "IBM Plex Sans",system-ui,-apple-system,"Segoe UI",sans-serif}
  .ck-in{max-width:1200px;margin:0 auto;padding:10px clamp(16px,4vw,32px);display:flex;flex-wrap:wrap;align-items:center;justify-content:space-between;gap:8px 20px}
  .ck p{margin:0;flex:1 1 300px}.ck a{color:#fff;text-underline-offset:3px}
  .ck-b{display:flex;gap:8px;flex:0 0 auto}
  .ck button{min-width:104px;min-height:44px;padding:0 18px;border-radius:999px;font:600 14.5px/1.2 inherit;font-family:inherit;cursor:pointer;border:1.5px solid #fff}
  .ck .ck-yes{background:#fff;color:#0e1b24}.ck .ck-no{background:transparent;color:#fff}
  .ck button:focus-visible,.ck a:focus-visible{outline:3px solid #ff5a36;outline-offset:2px}
  @media (max-width:560px){.ck-b{flex:1 1 100%}.ck button{flex:1 1 0}}`;

  function banner(fromLink) {
    if (document.querySelector(".ck")) return;
    if (!document.getElementById("ck-css")) { const st = document.createElement("style"); st.id = "ck-css"; st.textContent = css; document.head.appendChild(st); }
    const box = document.createElement("section");
    box.className = "ck"; box.setAttribute("aria-label", "Cookie choice");
    box.innerHTML = `<div class="ck-in"><p>May we use Google Analytics cookies to count visits? They stay off unless you accept. <a href="/privacy.html#cookies">Privacy notice</a></p>
      <div class="ck-b"><button type="button" class="ck-no">Reject</button><button type="button" class="ck-yes">Accept</button></div></div>`;
    // first in the page, so a keyboard or screen reader reaches it before anything else; it is drawn along the bottom edge
    document.body.insertBefore(box, document.body.firstChild);
    const back = fromLink ? document.activeElement : null;
    const close = () => { box.remove(); document.documentElement.style.removeProperty("--ck-h"); if (back && back.focus) back.focus(); };
    document.documentElement.style.setProperty("--ck-h", box.offsetHeight + "px");
    box.querySelector(".ck-yes").addEventListener("click", () => { save("granted"); close(); startAnalytics(); });
    box.querySelector(".ck-no").addEventListener("click", () => {
      const was = loaded; save("denied"); close();
      gtag("consent", "update", { analytics_storage: "denied" }); clearCookies();
      if (was) location.reload();   // stop a script that was already running
    });
    if (fromLink) box.querySelector(".ck-no").focus();
  }

  const choice = read();
  if (choice === "granted") startAnalytics();
  ready(() => {
    if (!choice) banner(false);
    document.addEventListener("click", e => { const link = e.target.closest(".js-cookie-settings"); if (link) { e.preventDefault(); banner(true); } });
  });
})();
