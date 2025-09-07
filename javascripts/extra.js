document.addEventListener("DOMContentLoaded", function() {
  const heroContainer = document.querySelector('.parallax');
  const contentPane = document.getElementById('content-pane');
  const scrollIndicator = document.querySelector('.scroll-indicator-wrapper');

  if (!heroContainer || !contentPane || !scrollIndicator) {
    return;
  }

  const heroElements = Array.from(heroContainer.children);
  const fadeDistance = 400; // The scroll distance over which to fade/blur

  // Calculate the scroll position where the animation should start.
  // This is when the bottom of the scroll indicator is about to leave the viewport.
  // We subtract the viewport height to find the scrollY value and ensure it's not negative.
  const startScroll = Math.max(0, scrollIndicator.offsetTop + scrollIndicator.offsetHeight - window.innerHeight);

  const handleScroll = () => {
    const scrollPosition = window.pageYOffset;

    // Calculate the animation's progress (0 to 1)
    let progress = 0;
    if (scrollPosition > startScroll) {
      progress = (scrollPosition - startScroll) / fadeDistance;
    }
    progress = Math.min(progress, 1); // Clamp to a max of 1

    const heroOpacity = 1 - progress;
    const heroBlur = progress * 5; // blur up to 5px

    heroElements.forEach(el => {
      el.style.opacity = heroOpacity;
      el.style.filter = `blur(${heroBlur}px)`;
    });

    contentPane.style.opacity = progress;
  };

  window.addEventListener('scroll', handleScroll, { passive: true });

  // Set the initial state on page load
  handleScroll();
});
