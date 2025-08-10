document.addEventListener("DOMContentLoaded", function() {
  // --- Logic for revealing content sections ---
  const sections = document.querySelectorAll('#content-pane .section');
  if (sections.length > 0) {
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
  }

  // --- Logic for fading hero content on scroll ---
  const heroContainer = document.querySelector('.parallax');
  if (!heroContainer) return;

  const heroElements = Array.from(heroContainer.children);

  window.addEventListener('scroll', function() {
    const scrollPosition = window.pageYOffset;
    const fadeDistance = 400; // The scroll distance over which to fade/blur

    let newOpacity = 1;
    let newBlur = 0;

    if (scrollPosition <= fadeDistance) {
      newOpacity = 1 - scrollPosition / fadeDistance;
      newBlur = (scrollPosition / fadeDistance) * 5; // blur up to 5px
    } else {
      newOpacity = 0;
      newBlur = 5;
    }

    heroElements.forEach(el => {
      el.style.opacity = newOpacity;
      el.style.filter = `blur(${newBlur}px)`;
    });
  }, { passive: true }); // Improve scroll performance
});
