// Parallax scroll effect with fallback for unsupported browsers and headless Chromium
//
// This implements a parallax effect where hero elements (profile image, name, subtitle)
// fade out and blur as the user scrolls past the contact section, while the content
// pane fades in. Two implementations are available:
//
// 1. CSS scroll-driven animations (modern browsers)
//    - Uses `animation-timeline: view()` and `animation-range`
//    - Supported in Chrome/Edge 115+, Safari 17+, Firefox (with flag)
//    - See: https://developer.mozilla.org/en-US/docs/Web/CSS/animation-timeline
//
// 2. JavaScript fallback (all other browsers)
//    - Uses scroll event listener with requestAnimationFrame
//    - Manages opacity and blur based on scroll position
//    - Adds 'js-parallax-fallback' class to body
//
// Browser detection logic:
// - Checks for `animation-timeline: view()` AND `animation-range` support
// - Detects headless browsers (automated testing, CI)
// - Firefox partial support detection (scroll() but no animation-range)
// - Manual override via URL: ?parallax=css or ?parallax=js
// - Debug mode: ?debug=parallax or localStorage.debugParallax = 'true'
//
// Common issues:
// - Chrome/Edge 115+ should support CSS animations natively
// - Firefox requires flag: layout.css.scroll-driven-animations.enabled = true
// - Safari 17+ supports CSS animations
// - Older browsers use JavaScript fallback
// - Headless detection may be too aggressive (removed 800x600 check)
//
document.addEventListener("DOMContentLoaded", function() {
  const heroContainer = document.querySelector('.parallax');
  const contentPane = document.getElementById('content-pane');
  const scrollIndicator = document.querySelector('.scroll-indicator-wrapper');
  const contact = document.getElementById('contact');

  if (!heroContainer || !contentPane || !scrollIndicator || !contact) {
    return;
  }

  // Get URL parameters for debugging and overrides
  const urlParams = new URLSearchParams(window.location.search);
  const debugParallax = urlParams.has('debug') && urlParams.get('debug').includes('parallax');
  const forceParallaxMode = urlParams.get('parallax'); // 'css' or 'js'

  // Detect if CSS scroll-driven animations are both supported AND likely to work
  // (i.e., not in headless/automation environment where they may be broken)
  // Firefox partially supports animation-timeline but not animation-range
  const hasAnimationRangeSupport =
    CSS.supports('animation-range', '0% 100%') ||
    CSS.supports('animation-range', 'exit 0px 400px');
  const hasFullScrollAnimationsSupport =
    CSS.supports('animation-timeline', 'view()') &&
    hasAnimationRangeSupport;
  const isHeadless = () => {
    // navigator.webdriver is true when browser is automated (headless or not)
    if (navigator.webdriver) return true;
    // User agent may contain "HeadlessChrome"
    if (navigator.userAgent.includes('HeadlessChrome')) return true;
    // Check for headless patterns in user agent (common in CI environments)
    if (navigator.userAgent.includes('Headless') || navigator.userAgent.includes('PhantomJS')) return true;
    return false;
  };

    let shouldUseCSSAnimations = hasFullScrollAnimationsSupport && !isHeadless();
    let parallaxMode;

    // Apply manual override if specified
    if (forceParallaxMode === 'css') {
      shouldUseCSSAnimations = true;
      parallaxMode = 'css';
      if (debugParallax || localStorage.getItem('debugParallax') === 'true') {
        console.log(`Manual override: forcing CSS parallax mode`);
      }
    } else if (forceParallaxMode === 'js') {
      shouldUseCSSAnimations = false;
      parallaxMode = 'js';
      if (debugParallax || localStorage.getItem('debugParallax') === 'true') {
        console.log(`Manual override: forcing JS parallax mode`);
      }
    } else {
      parallaxMode = shouldUseCSSAnimations ? 'css' : 'js';
    }

  // Debug logging for parallax detection
  if (debugParallax || localStorage.getItem('debugParallax') === 'true') {
    console.log('=== PARALLAX DIAGNOSTICS ===');
    console.log('Browser:', navigator.userAgent);
    console.log('CSS.supports checks:');
    console.log('  animation-timeline: view()', CSS.supports('animation-timeline', 'view()'));
    console.log('  animation-range: 0% 100%', CSS.supports('animation-range', '0% 100%'));
    console.log('  animation-range: exit 0px exit 400px', CSS.supports('animation-range', 'exit 0px exit 400px'));
    console.log('  animation-range: exit 0px 400px', CSS.supports('animation-range', 'exit 0px 400px'));
    console.log('  animation-range: exit 0% exit 100%', CSS.supports('animation-range', 'exit 0% exit 100%'));
    console.log('  animation-range: exit 0% 100%', CSS.supports('animation-range', 'exit 0% 100%'));
    console.log('  view-timeline-name: --test', CSS.supports('view-timeline-name', '--test'));
    console.log('  view-timeline: --test block', CSS.supports('view-timeline', '--test block'));

    console.log('\nDetection results:');
    console.log('  hasFullScrollAnimationsSupport:', hasFullScrollAnimationsSupport);
    console.log('  isHeadless():', isHeadless());
    console.log('  shouldUseCSSAnimations:', shouldUseCSSAnimations);
    console.log('  parallaxMode:', parallaxMode);



    // Check if CSS animations are actually applied
    if (heroContainer) {
      const heroElement = heroContainer.querySelector('.hero') || heroContainer.children[0];
      if (heroElement) {
        const computedStyle = window.getComputedStyle(heroElement);
        console.log('\nComputed styles for hero element:');
        console.log('  animation-name:', computedStyle.animationName);
        console.log('  animation-timeline:', computedStyle.animationTimeline);
        console.log('  animation-range:', computedStyle.animationRange);
        console.log('  opacity:', computedStyle.opacity);
        console.log('  filter:', computedStyle.filter);

        // Check view timeline registration on #contact
        const contact = document.getElementById('contact');
        if (contact) {
          const contactStyle = window.getComputedStyle(contact);
          console.log('\nView timeline registration on #contact:');
          console.log('  view-timeline-name:', contactStyle.viewTimelineName);
          console.log('  view-timeline-axis:', contactStyle.viewTimelineAxis);
          console.log('  view-timeline:', contactStyle.viewTimeline);
        }

        // Check which CSS rule is winning
        console.log('\nActive @supports blocks:');
        console.log('  animation-timeline: view() supported:', CSS.supports('animation-timeline', 'view()'));
        console.log('  animation-timeline: view() NOT supported:', CSS.supports('not (animation-timeline: view())'));
      }
    }
    console.log('=== END DIAGNOSTICS ===\n');
  }

  // Firefox detection for partial scroll-driven animations support
  const isFirefox = navigator.userAgent.includes('Firefox');
  const hasPartialFirefoxSupport = isFirefox &&
    CSS.supports('animation-timeline', 'scroll()') &&
    !CSS.supports('animation-range', '0% 100%');
  if (hasPartialFirefoxSupport && (debugParallax || localStorage.getItem('debugParallax') === 'true')) {
    console.warn('Firefox detected with partial scroll-driven animations support. Enable full support with flag: layout.css.scroll-driven-animations.enabled = true');
  }



  // Function to activate JavaScript fallback
  const activateJSFallback = () => {
    if (debugParallax || localStorage.getItem('debugParallax') === 'true') {
      console.log('Activating JavaScript parallax fallback');
    }
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
    if (debugParallax || localStorage.getItem('debugParallax') === 'true') {
      console.log('CSS scroll-driven animations are supported, checking if applied...');
    }
    // Check if CSS animations are actually applied
    const heroElement = heroContainer.querySelector('.hero') || heroContainer.children[0];
    if (heroElement) {
      const computedStyle = window.getComputedStyle(heroElement);
      const animationName = computedStyle.animationName;
      const animationTimeline = computedStyle.animationTimeline;
      const animationRange = computedStyle.animationRange;

      // If no animation is applied (or animation is 'none'), fall back to JS
      if (!animationName || animationName === 'none' || !animationTimeline || animationTimeline === 'none' || animationTimeline === 'auto' || !animationRange) {
        if (debugParallax || localStorage.getItem('debugParallax') === 'true') {
          console.log('CSS animations not properly applied, falling back to JS', { animationName, animationTimeline, animationRange });
        }
        shouldUseCSSAnimations = false;
        parallaxMode = 'js';
        activateJSFallback();
      } else {
        // CSS animations are working
        if (debugParallax || localStorage.getItem('debugParallax') === 'true') {
          console.log('CSS scroll-driven animations are active', { animationName, animationTimeline, animationRange });
        }
        parallaxMode = 'css';
        // Rely on CSS entirely (do nothing)
      }
    } else {
      // No hero element found, use JS fallback
      if (debugParallax || localStorage.getItem('debugParallax') === 'true') {
        console.log('No hero element found, using JS fallback');
      }
      parallaxMode = 'js';
      activateJSFallback();
    }
  } else {
    // CSS animations not supported or headless detected
    if (debugParallax || localStorage.getItem('debugParallax') === 'true') {
      console.log('CSS scroll-driven animations not supported or headless detected, using JS fallback');
    }
    parallaxMode = 'js';
    activateJSFallback();
  }


});
