document.addEventListener("DOMContentLoaded", function() {
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
    root: null, // use the viewport as the root
    threshold: 0.1, // Start animation when 10% of the element is visible
    rootMargin: '0px 0px -50px 0px' // Trigger a bit before it's fully in view
  });

  sections.forEach(section => {
    observer.observe(section);
  });
});
