/* Iterra Maps — prices in US dollars or euro.
   The pages are written in dollars. Visitors whose browser is set to a European time zone see euro.
   The € / $ switch overrides that, and the choice is remembered in this browser.
   Any element with data-usd and data-eur gets the matching text (or value, for form inputs). */
(function () {
  const KEY = "iterra.currency";
  function detect() {
    try { const v = localStorage.getItem(KEY); if (v === "usd" || v === "eur") return v; } catch (e) {}
    let tz = "";
    try { tz = Intl.DateTimeFormat().resolvedOptions().timeZone || ""; } catch (e) {}
    return /^Europe\//.test(tz) || /^Atlantic\/(Azores|Madeira|Canary|Faroe|Reykjavik)$/.test(tz) ? "eur" : "usd";
  }
  function apply(cur) {
    document.documentElement.dataset.currency = cur;
    document.querySelectorAll("[data-usd][data-eur]").forEach(el => {
      const v = el.getAttribute("data-" + cur);
      if (el.tagName === "INPUT") el.value = v; else el.textContent = v;
    });
    document.querySelectorAll(".js-cur").forEach(b => b.setAttribute("aria-pressed", String(b.dataset.cur === cur)));
  }
  function start() {
    apply(detect());
    document.addEventListener("click", e => {
      const b = e.target.closest(".js-cur"); if (!b) return;
      try { localStorage.setItem(KEY, b.dataset.cur); } catch (err) {}
      apply(b.dataset.cur);
    });
  }
  document.readyState === "loading" ? document.addEventListener("DOMContentLoaded", start) : start();
})();
