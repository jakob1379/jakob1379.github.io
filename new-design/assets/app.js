(() => {
  const yearTargets = document.querySelectorAll("[data-current-year]");
  yearTargets.forEach((target) => {
    target.textContent = new Date().getFullYear();
  });

  document.querySelectorAll("[data-copy-email]").forEach((button) => {
    const originalText = button.textContent;

    button.addEventListener("click", async () => {
      const email = button.getAttribute("data-copy-email");
      if (!email) {
        return;
      }

      try {
        await navigator.clipboard.writeText(email);
        button.textContent = "Email copied";
        window.setTimeout(() => {
          button.textContent = originalText;
        }, 1800);
      } catch {
        window.location.href = `mailto:${email}`;
      }
    });
  });

  document.querySelectorAll("[data-filter-group]").forEach((group) => {
    const buttons = group.querySelectorAll("[data-filter-value]");
    const targetSelector = group.getAttribute("data-filter-target");
    if (!targetSelector) {
      return;
    }

    let items;
    try {
      items = document.querySelectorAll(targetSelector);
    } catch {
      return;
    }

    buttons.forEach((button) => {
      button.addEventListener("click", () => {
        const value = button.getAttribute("data-filter-value");
        buttons.forEach((candidate) => {
          candidate.setAttribute("aria-pressed", String(candidate === button));
        });
        items.forEach((item) => {
          const tags = (item.getAttribute("data-tags") || "").split(/\s+/);
          item.hidden = value !== "all" && !tags.includes(value);
        });
      });
    });
  });
})();
