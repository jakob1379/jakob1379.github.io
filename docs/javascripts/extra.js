// Parallax scroll effect with fallback for unsupported browsers and headless Chromium
document.addEventListener("DOMContentLoaded", function() {
  const heroContainer = document.querySelector('.parallax');
  const contentPane = document.getElementById('content-pane');
  const scrollIndicator = document.querySelector('.scroll-indicator-wrapper');
  const contact = document.getElementById('contact');

  if (!heroContainer || !contentPane || !scrollIndicator || !contact) {
    return;
  }

  // Detect if CSS scroll-driven animations are both supported AND likely to work
  // (i.e., not in headless/automation environment where they may be broken)
  const cssScrollAnimationsSupported = CSS.supports('animation-timeline', 'view()');
  const isHeadless = () => {
    // navigator.webdriver is true when browser is automated (headless or not)
    if (navigator.webdriver) return true;
    // Typical headless viewport dimensions (800x600 inner)
    if (window.innerWidth === 800 && window.innerHeight === 600) return true;
    // User agent may contain "HeadlessChrome"
    if (navigator.userAgent.includes('HeadlessChrome')) return true;
    return false;
  };

  let shouldUseCSSAnimations = cssScrollAnimationsSupported && !isHeadless();

  // Function to activate JavaScript fallback
  const activateJSFallback = () => {
    document.body.classList.add('js-parallax-fallback');

    const heroElements = Array.from(heroContainer.children).filter(el => el.id !== 'contact' && el !== scrollIndicator);
    const fadeDistance = 400; // The scroll distance over which to fade/blur

    // Calculate the scroll position where the animation should start.
    // This is when the bottom of the contact section is about to leave the viewport.
    // We subtract the viewport height to find the scrollY value and ensure it's not negative.
    const rect = contact.getBoundingClientRect();
    const contactBottom = rect.top + rect.height + window.pageYOffset;
    const startScroll = Math.max(0, contactBottom - window.innerHeight);

    let ticking = false;
    let rafId = null;

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

      scrollIndicator.style.opacity = 0.5 * heroOpacity;

      contentPane.style.opacity = progress;
    };

    const requestTick = () => {
      if (!ticking) {
        ticking = true;
        rafId = requestAnimationFrame(() => {
          handleScroll();
          ticking = false;
        });
      }
    };

    window.addEventListener('scroll', requestTick, { passive: true });

    // Set the initial state on page load
    handleScroll();
  };

  // If CSS animations should be used, verify they're actually working
  if (shouldUseCSSAnimations) {
    // Check if CSS animations are actually applied
    const heroElement = heroContainer.querySelector('.hero') || heroContainer.children[0];
    if (heroElement) {
      const computedStyle = window.getComputedStyle(heroElement);
      const animationName = computedStyle.animationName;
      const animationTimeline = computedStyle.animationTimeline;

      // If no animation is applied (or animation is 'none'), fall back to JS
      if (!animationName || animationName === 'none' || !animationTimeline || animationTimeline === 'none') {
        shouldUseCSSAnimations = false;
        activateJSFallback();
      }
      // Otherwise, rely on CSS entirely (do nothing)
    } else {
      // No hero element found, use JS fallback
      activateJSFallback();
    }
  } else {
    // CSS animations not supported or headless detected
    activateJSFallback();
  }
});
