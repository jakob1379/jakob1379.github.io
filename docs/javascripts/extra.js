(() => {
  const enhancePage = () => {
    const header = document.querySelector(".site-nav");
    if (header && header.dataset.enhanced !== "true") {
      header.dataset.enhanced = "true";
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
    }
  };

  document.addEventListener("DOMContentLoaded", enhancePage, { once: true });
  document.addEventListener("zensical-instant-navigation", enhancePage);
})();
