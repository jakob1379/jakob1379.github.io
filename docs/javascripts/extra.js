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

  const contentPane = document.getElementById('content-pane');
  const heroElements = Array.from(heroContainer.children);

  const handleScroll = () => {
    const scrollPosition = window.pageYOffset;
    const fadeDistance = 400; // The scroll distance over which to fade/blur

    let heroOpacity = 1;
    let heroBlur = 0;

    if (scrollPosition <= fadeDistance) {
      heroOpacity = 1 - scrollPosition / fadeDistance;
      heroBlur = (scrollPosition / fadeDistance) * 5; // blur up to 5px
    } else {
      heroOpacity = 0;
      heroBlur = 5;
    }

    heroElements.forEach(el => {
      el.style.opacity = heroOpacity;
      el.style.filter = `blur(${heroBlur}px)`;
    });

    if (contentPane) {
      let contentOpacity = 0;
      if (scrollPosition <= fadeDistance) {
        contentOpacity = scrollPosition / fadeDistance;
      } else {
        contentOpacity = 1;
      }
      contentPane.style.opacity = contentOpacity;
    }
  };

  window.addEventListener('scroll', handleScroll, { passive: true });

  // --- Add smooth scroll for scroll-down button ---
  const scrollLink = document.querySelector('.scroll-indicator-wrapper a');
  if (scrollLink && contentPane) {
    scrollLink.addEventListener('click', function(e) {
      e.preventDefault();
      window.scrollTo({
        top: contentPane.offsetTop,
        behavior: 'smooth'
      });
    });
  }

  // Set the initial state on page load
  handleScroll();
});
