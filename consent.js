/* Iterra Maps — Google Analytics, only with the visitor's permission.
   Until GA_ID below is set to your real Measurement ID (G-…), this file does nothing:
   no banner, no "Cookie settings" link, no Google requests.
   Choice is kept in this browser for 12 months, then we ask again. */
(function () {
  const GA_ID = "G-GKXKNKSLET";               // ← paste your Measurement ID here
  const KEY = "iterra.consent";
  const MAX_AGE = 365 * 24 * 3600 * 1000;
  const enabled = /^G-[A-Z0-9]{6,}$/.test(GA_ID) && !/^G-X+$/.test(GA_ID);

  function ready(fn) { document.readyState === "loading" ? document.addEventListener("DOMContentLoaded", fn) : fn(); }
  if (!enabled) {
    ready(() => document.querySelectorAll(".js-cookie-settings").forEach(el => (el.closest("li") || el).remove()));
    return;
  }

  function read() {
    try {
      const v = JSON.parse(localStorage.getItem(KEY) || "null");
      return v && (v.c === "granted" || v.c === "denied") && Date.now() - v.t < MAX_AGE ? v.c : null;
    } catch (e) { return null; }
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
    const s = document.createElement("script");
    s.async = true;
    s.src = "https://www.googletagmanager.com/gtag/js?id=" + GA_ID;
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

  const privacy = location.pathname.includes("/for/") ? "../../privacy.html" : "/privacy.html";
  const css = `
  .ck{position:fixed;z-index:100;left:16px;right:16px;bottom:16px;max-width:560px;margin:0 auto;background:#0e1b24;color:#dfe6ea;
      border-radius:16px;padding:18px 20px;box-shadow:0 10px 40px rgba(0,0,0,.28);font:400 15px/1.5 system-ui,-apple-system,"Segoe UI",sans-serif}
  .ck p{margin:0 0 14px}.ck a{color:#fff;text-underline-offset:3px}
  .ck-b{display:flex;gap:10px;flex-wrap:wrap}
  .ck button{flex:1 1 140px;min-height:44px;border-radius:999px;font-family:inherit;font-size:15px;font-weight:600;line-height:1.2;cursor:pointer;border:1.5px solid #fff}
  .ck .ck-yes{background:#fff;color:#0e1b24}.ck .ck-no{background:transparent;color:#fff}
  .ck button:focus-visible{outline:3px solid #ff5a36;outline-offset:2px}`;

  function banner() {
    if (document.querySelector(".ck")) return;
    if (!document.getElementById("ck-css")) {
      const st = document.createElement("style"); st.id = "ck-css"; st.textContent = css; document.head.appendChild(st);
    }
    const box = document.createElement("div");
    box.className = "ck"; box.setAttribute("role", "dialog"); box.setAttribute("aria-label", "Cookie choice");
    box.innerHTML = `<p>We’d like to use Google Analytics cookies to count visits and see which pages people find useful. They stay off unless you accept. <a href="${privacy}#cookies">More in our privacy notice</a>.</p>
      <div class="ck-b"><button type="button" class="ck-no">Reject</button><button type="button" class="ck-yes">Accept</button></div>`;
    document.body.appendChild(box);
    box.querySelector(".ck-yes").addEventListener("click", () => { save("granted"); box.remove(); startAnalytics(); });
    box.querySelector(".ck-no").addEventListener("click", () => {
      const was = loaded; save("denied"); box.remove();
      gtag("consent", "update", { analytics_storage: "denied" }); clearCookies();
      if (was) location.reload();   // stop a script that was already running
    });
  }

  const choice = read();
  if (choice === "granted") startAnalytics();
  ready(() => {
    if (!choice) banner();
    document.addEventListener("click", e => {
      const link = e.target.closest(".js-cookie-settings");
      if (link) { e.preventDefault(); banner(); }
    });
  });
})();
