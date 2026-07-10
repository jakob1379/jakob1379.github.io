(() => {
  const enhancePage = () => {
    document.querySelectorAll("[data-current-year]").forEach((target) => {
      target.textContent = new Date().getFullYear();
    });

    const header = document.querySelector(".site-nav");
    if (header && header.dataset.enhanced !== "true") {
      header.dataset.enhanced = "true";
      const navToggle = header.querySelector("[data-nav-toggle]");
      const navLinks = header.querySelectorAll(".nav-links a");
      let frame = 0;
      const updateDepth = () => {
        frame = 0;
        header.dataset.scrolled = String(window.scrollY > 24);
      };
      const queueDepthUpdate = () => {
        if (!frame) {
          frame = window.requestAnimationFrame(updateDepth);
        }
      };
      updateDepth();
      window.addEventListener("scroll", queueDepthUpdate, { passive: true });

      if (navToggle) {
        navToggle.addEventListener("click", () => {
          const isOpen = header.dataset.menuOpen === "true";
          header.dataset.menuOpen = String(!isOpen);
          navToggle.setAttribute("aria-expanded", String(!isOpen));
        });

        navLinks.forEach((link) => {
          link.addEventListener("click", () => {
            header.dataset.menuOpen = "false";
            navToggle.setAttribute("aria-expanded", "false");
          });
        });
      }
    }
  };

  document.addEventListener("DOMContentLoaded", enhancePage, { once: true });
  document.addEventListener("zensical-instant-navigation", enhancePage);
})();
