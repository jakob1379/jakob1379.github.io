// Chromium and WebKit slide the active nav underline across a real navigation
// via the @view-transition rule in CSS. Firefox has no cross-document view
// transitions, and its same-document ones do not animate a group's position,
// so there the underline is slid with an ordinary CSS transition instead:
// remember which item we left from, start the new page's underline at that
// offset, and let it travel home on the next frame.
(() => {
  if (typeof CSSViewTransitionRule !== "undefined") {
    return;
  }
  if (!window.matchMedia("(prefers-reduced-motion: no-preference)").matches) {
    return;
  }

  const ORIGIN_KEY = "nav-underline-origin";

  const slideUnderline = () => {
    const links = [...document.querySelectorAll(".nav-links a")];
    const active = document.querySelector(".nav-links a[aria-current]");

    links.forEach((link) => {
      link.addEventListener("click", () => {
        // Same-page anchors do not navigate, so they leave nothing behind.
        const target = new URL(link.href, location.href);
        if (target.pathname === location.pathname) {
          return;
        }
        if (active) {
          sessionStorage.setItem(ORIGIN_KEY, String(links.indexOf(active)));
        }
      });
    });

    const origin = links[Number(sessionStorage.getItem(ORIGIN_KEY))];
    sessionStorage.removeItem(ORIGIN_KEY);
    if (!active || !origin || origin === active) {
      return;
    }

    // Both links share .site-nav as their offset parent, so this is the gap
    // between where the underline was and where it belongs.
    const distance = origin.offsetLeft - active.offsetLeft;
    if (!distance) {
      return;
    }

    active.classList.add("nav-underline-instant");
    active.style.setProperty("--nav-slide", `${distance}px`);
    void active.offsetWidth;
    active.classList.remove("nav-underline-instant");
    active.style.setProperty("--nav-slide", "0px");
  };

  document.addEventListener("DOMContentLoaded", slideUnderline, { once: true });
  document.addEventListener("zensical-instant-navigation", slideUnderline);
})();
