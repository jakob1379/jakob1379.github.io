from pathlib import Path
import re

import pytest
from playwright.sync_api import expect


NEWPAGE_PATH = Path("newpage/index.html").absolute()


def open_newpage(page):
    page.goto(f"file://{NEWPAGE_PATH}")
    page.wait_for_load_state("networkidle")


def test_newpage_science_enabler_positioning(page, browser_name):
    if browser_name == "webkit":
        pytest.skip("webkit browser not available in nix environment")

    open_newpage(page)

    expect(
        page.get_by_role(
            "heading",
            name="Science enabler.",
        )
    ).to_be_visible()
    expect(page.get_by_text("Backend, data, and simple tools for scientific teams")).to_be_visible()
    expect(page.get_by_text("Science enabler / tools / backend")).to_be_visible()
    expect(page.locator("[data-email-link]").first).to_have_attribute(
        "href",
        re.compile(r"^mailto:"),
    )
    expect(page.get_by_role("link", name="LinkedIn")).to_have_attribute(
        "href",
        "https://www.linkedin.com/in/jakobguldberg/",
    )


def test_newpage_cv_grounded_evidence(page, browser_name):
    if browser_name == "webkit":
        pytest.skip("webkit browser not available in nix environment")

    open_newpage(page)

    expect(page.locator("[data-case]")).to_have_count(4)
    expect(page.get_by_role("heading", name="Selected work.")).to_be_visible()
    expect(page.get_by_text("20,000 scientific articles in 3 hours")).to_be_visible()
    expect(page.get_by_text("Snakemake pipeline into an installable Python/Prefect workflow")).to_be_visible()
    expect(page.get_by_text("FastAPI, React, SQLAlchemy/Alembic")).to_be_visible()
    expect(page.get_by_text("uv, Nix, OCI images, Docker, Ansible, Slurm")).to_be_visible()


def test_newpage_mobile_nav(page, browser_name):
    if browser_name == "webkit":
        pytest.skip("webkit browser not available in nix environment")

    page.set_viewport_size({"width": 375, "height": 812})
    open_newpage(page)

    menu = page.get_by_role("button", name="Menu")
    expect(menu).to_have_attribute("aria-expanded", "false")

    menu.click()
    expect(menu).to_have_attribute("aria-expanded", "true")

    page.get_by_role("link", name="Evidence").click()
    expect(menu).to_have_attribute("aria-expanded", "false")
