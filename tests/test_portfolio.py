from pathlib import Path

import pytest
from playwright.sync_api import expect


PORTFOLIO_PATH = Path("site/index.html").absolute()


def open_portfolio(page):
    page.goto(f"file://{PORTFOLIO_PATH}")
    page.wait_for_load_state("networkidle")


def test_portfolio_science_enabler_positioning(page, browser_name):
    if browser_name == "webkit":
        pytest.skip("webkit browser not available in nix environment")

    open_portfolio(page)

    expect(
        page.get_by_role(
            "heading",
            name="Science enabler.",
        )
    ).to_be_visible()
    expect(page.get_by_text("Backend, data, and simple tools for scientific teams")).to_be_visible()
    expect(page.get_by_text("Science enabler / tools / backend")).to_be_visible()
    hero_actions = page.locator(".hero .actions")
    expect(hero_actions.get_by_role("link", name="Email Jakob")).to_have_attribute(
        "href",
        "mailto:jakob1379+jgalabs@gmail.com",
    )
    expect(hero_actions.get_by_role("link", name="GitHub")).to_have_attribute(
        "href",
        "https://github.com/jakob1379",
    )
    expect(hero_actions.get_by_role("link", name="LinkedIn")).to_have_attribute(
        "href",
        "https://www.linkedin.com/in/jakobguldberg/",
    )
    expect(hero_actions.get_by_role("link", name="Download CV")).to_have_class(
        "button cv-download"
    )
    expect(page.get_by_text("Start a role conversation")).to_have_count(0)
    expect(page.get_by_text("Copy email")).to_have_count(0)


def test_portfolio_cv_grounded_evidence(page, browser_name):
    if browser_name == "webkit":
        pytest.skip("webkit browser not available in nix environment")

    open_portfolio(page)

    expect(page.locator("[data-case]")).to_have_count(4)
    expect(page.get_by_role("heading", name="Selected work.")).to_be_visible()
    expect(page.get_by_text("20,000 articles in 3 hours")).to_be_visible()
    expect(page.get_by_text("runnable internal tools for lab data, compute")).to_be_visible()
    expect(page.get_by_text("Snakemake pipeline into an installable Python/Prefect workflow")).to_be_visible()
    expect(page.get_by_text("FastAPI, React, SQLAlchemy/Alembic")).to_be_visible()
    expect(page.get_by_text("uv, Nix, OCI images, Docker, Ansible, Slurm")).to_be_visible()
    expect(page.get_by_alt_text("Evaxion logo")).to_have_attribute("src", "assets/evaxion.svg")
    expect(page.get_by_alt_text("SeeQ Diagnostics logo")).to_have_attribute(
        "src",
        "assets/seeq-diagnostics.svg",
    )


def test_portfolio_mobile_nav(page, browser_name):
    if browser_name == "webkit":
        pytest.skip("webkit browser not available in nix environment")

    page.set_viewport_size({"width": 375, "height": 812})
    open_portfolio(page)

    menu = page.get_by_role("button", name="Menu")
    expect(menu).to_have_attribute("aria-expanded", "false")

    menu.click()
    expect(menu).to_have_attribute("aria-expanded", "true")

    page.get_by_role("link", name="Contact").click()
    expect(menu).to_have_attribute("aria-expanded", "false")
