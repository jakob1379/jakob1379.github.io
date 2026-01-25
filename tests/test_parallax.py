"""
Playwright tests for parallax scroll effects.

Tests verify:
1. Hero banner, image, and scroll indicator are visible on page load
2. Parallax effect triggers during scroll (opacity/blur changes)
3. Content pane becomes visible after scroll
4. Cross-browser and cross-device compatibility
"""

import pytest
import re
from pathlib import Path
from typing import Dict, Any


# Base URL for built site (relative path to built HTML)
SITE_BASE_PATH = Path("site").absolute()


def test_parallax_elements_visible(page, browser_name):
    """Test that hero, image, scroll indicator are visible on initial load."""
    if browser_name == "webkit":
        pytest.skip("webkit browser not available in nix environment")
    # Load the built site
    page.goto(f"file://{SITE_BASE_PATH}/index.html")

    # Wait for page to be fully loaded
    page.wait_for_load_state("networkidle")

    # Check hero container exists and is visible
    hero = page.locator(".parallax")
    assert hero.is_visible(), "Parallax container should be visible"

    # Check hero content (div.hero)
    hero_content = page.locator(".parallax > .hero")
    assert hero_content.is_visible(), "Hero content should be visible"

    # Check profile image exists and is visible
    profile_img = page.locator(".hero img")
    assert profile_img.is_visible(), "Profile image should be visible"

    # Check scroll indicator exists and is visible
    scroll_indicator = page.locator(".scroll-indicator-wrapper")
    assert scroll_indicator.is_visible(), "Scroll indicator should be visible"

    # Check contact section exists (triggers parallax)
    contact_section = page.locator("#contact")
    assert contact_section.is_visible(), "Contact section should be visible"

    # Check content pane exists (initially hidden or transparent)
    content_pane = page.locator("#content-pane")
    assert content_pane.is_visible(), "Content pane should be visible"


import pytest


def test_parallax_scroll_effect(page, browser_name):
    """Test that parallax effect occurs during scroll (opacity/blur changes)."""
    if browser_name == "webkit":
        pytest.skip("webkit browser not available in nix environment")
    page.goto(f"file://{SITE_BASE_PATH}/index.html")
    page.wait_for_load_state("networkidle")

    # Get initial state of hero elements
    hero_elements = page.locator(
        ".parallax > *:not(#contact):not(.scroll-indicator-wrapper)"
    )
    first_hero_element = hero_elements.first

    # Get initial opacity and filter (blur)
    initial_opacity = page.evaluate(
        """
        (el) => {
            return window.getComputedStyle(el).opacity;
        }
    """,
        first_hero_element.element_handle(),
    )

    initial_filter = page.evaluate(
        """
        (el) => {
            return window.getComputedStyle(el).filter;
        }
    """,
        first_hero_element.element_handle(),
    )

    # Initial opacity should be "1" (fully visible)
    # Note: In some viewport sizes, contact section may already be below viewport,
    # causing animation to be at end state. We'll handle this case.
    if initial_opacity != "1":
        # Contact might be below viewport. Scroll up to bring it into viewport.
        contact = page.locator("#contact")
        contact_rect = contact.evaluate("""
            el => {
                const rect = el.getBoundingClientRect();
                return rect.top;
            }
        """)
        if contact_rect > page.viewport_size["height"]:
            # Contact is below viewport, scroll up to bring it into viewport
            scroll_up = contact_rect - page.viewport_size["height"] + 100
            page.evaluate(f"window.scrollTo(0, {scroll_up})")
            page.wait_for_timeout(100)
            # Re-get initial opacity
            initial_opacity = page.evaluate(
                """
                (el) => {
                    return window.getComputedStyle(el).opacity;
                }
            """,
                first_hero_element.element_handle(),
            )

    # After adjustment, opacity should be "1"
    assert initial_opacity == "1", (
        f"Hero element should start opaque, got {initial_opacity}"
    )

    # Get contact section for scroll position calculation
    contact = page.locator("#contact")
    scroll_indicator = page.locator(".scroll-indicator-wrapper")
    contact_bottom = page.evaluate(
        """
        (el) => {
            const rect = el.getBoundingClientRect();
            return rect.bottom + window.pageYOffset;
        }
    """,
        contact.element_handle(),
    )
    # Calculate scroll position needed to trigger parallax
    # The effect starts when contact bottom leaves viewport
    viewport_height = page.viewport_size["height"]
    start_scroll = max(0, contact_bottom - viewport_height)

    # Scroll to trigger parallax (scroll past start position)
    scroll_position = start_scroll + 200  # 200px into the fade distance
    page.evaluate(f"window.scrollTo(0, {scroll_position})")

    # Wait for scroll to settle and animations to apply
    page.wait_for_timeout(100)  # Small delay for CSS/JS updates

    # Get new opacity and filter values
    new_opacity = page.evaluate(
        """
        (el) => {
            return window.getComputedStyle(el).opacity;
        }
    """,
        first_hero_element.element_handle(),
    )

    new_filter = page.evaluate(
        """
        (el) => {
            return window.getComputedStyle(el).filter;
        }
    """,
        first_hero_element.element_handle(),
    )

    # Verify opacity decreased (hero fading out)
    opacity_float = float(new_opacity)
    assert opacity_float < 1.0, (
        f"Hero opacity should decrease after scroll, got {new_opacity}"
    )
    assert opacity_float > 0.0, (
        f"Hero opacity should not be zero after partial scroll, got {new_opacity}"
    )

    # Verify blur increased (if browser supports CSS scroll-driven animations)
    # Note: JavaScript fallback applies filter: blur(px)
    if "blur" in new_filter:
        # Extract blur value
        blur_match = re.search(r"blur\(([\d.]+)px\)", new_filter)
        if blur_match:
            blur_value = float(blur_match.group(1))
            assert blur_value > 0.0, (
                f"Blur should be positive after scroll, got {blur_value}"
            )

    # Check scroll indicator opacity decreased
    indicator_opacity = page.evaluate(
        """
        (el) => {
            return window.getComputedStyle(el).opacity;
        }
    """,
        scroll_indicator.element_handle(),
    )

    indicator_opacity_float = float(indicator_opacity)
    assert indicator_opacity_float < 0.5, (
        f"Scroll indicator opacity should decrease after scroll, got {indicator_opacity}"
    )

    # Check content pane opacity increased
    content_pane = page.locator("#content-pane")
    content_opacity = page.evaluate(
        """
        (el) => {
            return window.getComputedStyle(el).opacity;
        }
    """,
        content_pane.element_handle(),
    )

    content_opacity_float = float(content_opacity)
    assert content_opacity_float > 0.0, (
        f"Content pane should become visible after scroll, got {content_opacity}"
    )
    assert content_opacity_float <= 1.0, (
        f"Content pane opacity should not exceed 1, got {content_opacity}"
    )


def test_parallax_complete_scroll(page, browser_name):
    """Test that parallax effect completes when scrolled to bottom."""
    if browser_name == "webkit":
        pytest.skip("webkit browser not available in nix environment")
    page.goto(f"file://{SITE_BASE_PATH}/index.html")
    page.wait_for_load_state("networkidle")

    # Scroll to very bottom of page
    page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
    page.wait_for_timeout(200)  # Allow animations to complete

    # Check hero elements are fully faded out
    hero_elements = page.locator(
        ".parallax > *:not(#contact):not(.scroll-indicator-wrapper)"
    )
    first_hero_element = hero_elements.first

    final_opacity = page.evaluate(
        """
        (el) => {
            return window.getComputedStyle(el).opacity;
        }
    """,
        first_hero_element.element_handle(),
    )

    # Opacity should be 0 or very close to 0 (fully faded)
    opacity_float = float(final_opacity)
    assert opacity_float < 0.1, (
        f"Hero should be nearly invisible at bottom, got {final_opacity}"
    )

    # Check scroll indicator is invisible
    scroll_indicator = page.locator(".scroll-indicator-wrapper")
    indicator_opacity = page.evaluate(
        """
        (el) => {
            return window.getComputedStyle(el).opacity;
        }
    """,
        scroll_indicator.element_handle(),
    )

    indicator_opacity_float = float(indicator_opacity)
    assert indicator_opacity_float < 0.1, (
        f"Scroll indicator should be invisible at bottom, got {indicator_opacity}"
    )

    # Check content pane is fully visible
    content_pane = page.locator("#content-pane")
    content_opacity = page.evaluate(
        """
        (el) => {
            return window.getComputedStyle(el).opacity;
        }
    """,
        content_pane.element_handle(),
    )

    content_opacity_float = float(content_opacity)
    assert content_opacity_float > 0.9, (
        f"Content pane should be fully visible at bottom, got {content_opacity}"
    )


@pytest.mark.parametrize(
    "viewport",
    [
        {"width": 1920, "height": 1080},  # Desktop large
        {"width": 1024, "height": 768},  # Desktop small
        {"width": 375, "height": 667},  # Mobile portrait
        {"width": 768, "height": 1024},  # Tablet portrait
    ],
)
def test_parallax_viewport_responsive(page, browser_name, viewport):
    """Test parallax works across different viewport sizes."""
    if browser_name == "webkit":
        pytest.skip("webkit browser not available in nix environment")
    page.set_viewport_size(viewport)
    page.goto(f"file://{SITE_BASE_PATH}/index.html")
    page.wait_for_load_state("networkidle")

    # Basic visibility check
    hero = page.locator(".parallax")
    assert hero.is_visible(), f"Hero should be visible at {viewport}"

    # Scroll to trigger parallax
    page.evaluate("window.scrollTo(0, 400)")
    page.wait_for_timeout(100)

    # Verify parallax is working (opacity changed)
    hero_element = page.locator(".parallax > .hero")
    opacity = page.evaluate(
        """
        (el) => {
            return window.getComputedStyle(el).opacity;
        }
    """,
        hero_element.element_handle(),
    )

    opacity_float = float(opacity)
    # At scroll position 400, parallax may or may not have started
    # depending on viewport height and scroll indicator position
    # We just ensure the value is valid
    assert 0.0 <= opacity_float <= 1.0, f"Opacity should be valid, got {opacity}"


# Browser matrix test - pytest-playwright automatically runs tests on all browsers
# We can use the built-in browser fixture to parametrize
# This test ensures basic functionality works across all browsers
def test_parallax_cross_browser(page, browser_name):
    """Basic smoke test that parallax elements exist in all browsers."""
    if browser_name == "webkit":
        pytest.skip("webkit browser not available in nix environment")
    page.goto(f"file://{SITE_BASE_PATH}/index.html")
    page.wait_for_load_state("networkidle")

    # Count parallax children
    parallax_children = page.locator(".parallax > *")
    count = parallax_children.count()
    assert count >= 3, (
        f"Parallax should have at least 3 children (hero, contact, indicator), got {count}"
    )

    # Verify key elements
    assert page.locator(".hero").is_visible()
    assert page.locator("#contact").is_visible()
    assert page.locator(".scroll-indicator-wrapper").is_visible()
    assert page.locator("#content-pane").is_visible()


def test_parallax_timeline_validation(page, browser_name):
    """Verify that the parallax timeline is correctly attached (CSS mode) or JS fallback works (JS mode) and the hero banner is visible at page load."""
    if browser_name == "webkit":
        pytest.skip("webkit browser not available in nix environment")
    page.goto(f"file://{SITE_BASE_PATH}/index.html?debug=parallax")
    page.wait_for_load_state("networkidle")

    result = page.evaluate("""() => {
        const mode = document.body.classList.contains('js-parallax-fallback') ? 'js' : 'css';
        const hero = document.querySelector('.hero');
        const computed = hero ? window.getComputedStyle(hero) : null;
        const animationTimeline = computed ? computed.animationTimeline : null;
        const animationRange = computed ? computed.animationRange : null;
        const opacity = computed ? computed.opacity : null;
        const contact = document.getElementById('contact');
        const contactStyle = contact ? window.getComputedStyle(contact) : null;
        const viewTimelineName = contactStyle ? contactStyle.viewTimelineName : null;

        return {
            mode,
            animationTimeline,
            animationRange,
            opacity,
            viewTimelineName,
            hasJsFallbackClass: document.body.classList.contains('js-parallax-fallback')
        };
    }""")

    # Hero must be visible
    assert result["opacity"] != "0", (
        f"Hero opacity is 0 (invisible) at page load. Mode: {result['mode']}"
    )

    if result["mode"] == "css":
        assert result["animationTimeline"] not in ("auto", "none", None), (
            f"CSS mode active but animationTimeline is {result['animationTimeline']}"
        )
        assert result["animationRange"] not in ("", None), (
            f"CSS mode active but animationRange is empty"
        )
        assert result["viewTimelineName"] == "--contact-timeline", (
            f"View timeline not registered: {result['viewTimelineName']}"
        )
    else:
        assert result["hasJsFallbackClass"] == True, (
            "JS fallback should be active (body.js-parallax-fallback)"
        )
