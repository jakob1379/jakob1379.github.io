from pathlib import Path

import pytest
from playwright.sync_api import expect


PORTFOLIO_PATH = Path("site/index.html").absolute()


def open_portfolio(page):
    page.goto(f"file://{PORTFOLIO_PATH}")
    page.wait_for_load_state("networkidle")


def test_portfolio_hero_leads_with_name_and_offer(page, browser_name):
    if browser_name == "webkit":
        pytest.skip("webkit browser not available in nix environment")

    open_portfolio(page)

    expect(page.get_by_role("heading", name="Tools scientists actually run.")).to_be_visible()
    expect(page.get_by_text("Jakob Stender Guldberg — science enabler")).to_be_visible()

    hero_actions = page.locator(".hero .actions")
    expect(hero_actions.get_by_role("link", name="Get in touch")).to_have_attribute(
        "href",
        "mailto:jakob1379+jgalabs@gmail.com",
    )
    expect(hero_actions.get_by_role("link", name="Download CV · PDF")).to_have_attribute(
        "href",
        "assets/Jakob_Stender_Guldberg_CV.pdf",
    )
    expect(hero_actions.get_by_role("link", name="GitHub")).to_have_attribute(
        "href",
        "https://github.com/jakob1379",
    )
    expect(hero_actions.get_by_role("link", name="LinkedIn")).to_have_attribute(
        "href",
        "https://www.linkedin.com/in/jakobguldberg/",
    )
    expect(hero_actions.get_by_role("link", name="PyPI")).to_have_attribute(
        "href",
        "https://pypi.org/user/jakob1379/",
    )


def test_portfolio_proof_rail_only_claims_real_numbers(page, browser_name):
    if browser_name == "webkit":
        pytest.skip("webkit browser not available in nix environment")

    open_portfolio(page)

    expect(page.locator(".proof")).to_have_count(2)
    expect(page.locator(".proof").first).to_contain_text("20,000")
    expect(page.locator(".capability")).to_have_count(2)


def test_portfolio_cases_are_attributed(page, browser_name):
    if browser_name == "webkit":
        pytest.skip("webkit browser not available in nix environment")

    open_portfolio(page)

    expect(page.locator("[data-case]")).to_have_count(3)
    expect(page.get_by_role("heading", name="Selected work.")).to_be_visible()
    expect(page.get_by_alt_text("Evaxion logo")).to_have_attribute("src", "assets/evaxion.svg")
    expect(page.get_by_alt_text("SeeQ Diagnostics logo")).to_have_attribute(
        "src",
        "assets/seeq-diagnostics.svg",
    )
    expect(page.locator(".case", has_text="SeeQ Diagnostics").get_by_role("link")).to_have_attribute(
        "href",
        "https://www.seeqdiagnostics.com/",
    )
    # The RegTech engagement cannot be named yet, so it has to say so rather than read as filler.
    expect(page.get_by_text("Client undisclosed")).to_be_visible()


def test_portfolio_ships_only_the_nav_transition_script(page, browser_name):
    if browser_name == "webkit":
        pytest.skip("webkit browser not available in nix environment")

    open_portfolio(page)

    scripts = page.locator("script")
    assert scripts.count() == 1
    # No inline script, so the CSP needs no hash to keep in sync.
    assert scripts.first.get_attribute("src") == "javascripts/nav-transition.js"
    assert (scripts.first.inner_text() or "").strip() == ""

    csp = page.locator("meta[http-equiv='Content-Security-Policy']").get_attribute("content")
    assert "script-src 'self'" in csp


def test_portfolio_navigation_needs_no_menu_button_on_mobile(page, browser_name):
    if browser_name == "webkit":
        pytest.skip("webkit browser not available in nix environment")

    page.set_viewport_size({"width": 375, "height": 812})
    open_portfolio(page)

    expect(page.get_by_role("button", name="Menu")).to_have_count(0)
    navigation = page.get_by_label("Primary navigation")
    for label in ("Portfolio", "Field notes", "Get in touch"):
        expect(navigation.get_by_role("link", name=label)).to_be_visible()
