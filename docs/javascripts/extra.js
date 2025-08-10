document.addEventListener("DOMContentLoaded", function() {
  // --- Logic for revealing content sections ---
  const sections = document.querySelectorAll('#content-pane .section');

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

    // Manually trigger reveal for sections that are in view
    if (sections.length > 0) {
      sections.forEach(section => {
        if (!section.classList.contains('visible')) {
          const rect = section.getBoundingClientRect();
          // Check if the top of the element is entering the viewport
          if (rect.top < window.innerHeight - 50) {
            section.classList.add('visible');
          }
        }
      });
    }
  };

  window.addEventListener('scroll', handleScroll, { passive: true });

  // --- Add smooth scroll for scroll-down button ---
  const scrollLink = document.querySelector('.scroll-indicator-wrapper a');
  if (scrollLink && contentPane) {
    // Custom easing function for a more pronounced acceleration and deceleration
    const easeInOutQuart = t => t < 0.5 ? 8 * t * t * t * t : 1 - 8 * (--t) * t * t * t;

    // Custom smooth scroll implementation
    const customSmoothScroll = (targetY, duration = 1200) => {
      const startY = window.pageYOffset;
      const distance = targetY - startY;
      let startTime = null;

      const animationStep = (currentTime) => {
        if (startTime === null) startTime = currentTime;
        const timeElapsed = currentTime - startTime;
        const progress = Math.min(timeElapsed / duration, 1);
        const easedProgress = easeInOutQuart(progress);

        window.scrollTo(0, startY + (distance * easedProgress));

        if (timeElapsed < duration) {
          requestAnimationFrame(animationStep);
        }
      };
      requestAnimationFrame(animationStep);
    };

    scrollLink.addEventListener('click', function(e) {
      e.preventDefault();
      customSmoothScroll(contentPane.offsetTop);
    });
  }

  // Set the initial state on page load
  handleScroll();
});
