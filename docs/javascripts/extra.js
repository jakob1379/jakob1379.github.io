document.addEventListener("DOMContentLoaded", function() {
  const scrollContainer = document.querySelector('.page-wrapper');
  if (!scrollContainer) return;

  const sections = document.querySelectorAll('#content-pane .section');
  if (sections.length === 0) {
    return;
  }

  const observer = new IntersectionObserver(entries => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('visible');
        observer.unobserve(entry.target);
      }
    });
  }, {
    root: scrollContainer,
    threshold: 0.1, // Start animation when 10% of the element is visible
  });

  sections.forEach(section => {
    observer.observe(section);
  });
});
