from pathlib import Path

from playwright.sync_api import expect


SITE_PATH = Path("site").absolute()
NAV_LABELS = ["Portfolio", "Contact", "Field notes"]


def open_site_page(page, path: str) -> None:
    page.goto(f"file://{SITE_PATH / path}")
    page.wait_for_load_state("networkidle")


def navigation_signature(page) -> dict[str, object]:
    return page.evaluate(
        """
        () => {
          const header = document.querySelector('.site-nav');
          const mark = document.querySelector('.brand-mark');
          const descriptor = document.querySelector('.brand span:last-child');
          const links = document.querySelector('.nav-links');
          const descriptorStyle = getComputedStyle(descriptor);
          const linksStyle = getComputedStyle(links);
          return {
            headerHeight: header.getBoundingClientRect().height,
            markWidth: mark.getBoundingClientRect().width,
            markHeight: mark.getBoundingClientRect().height,
            descriptorFont: descriptorStyle.fontFamily,
            descriptorSize: descriptorStyle.fontSize,
            descriptorSpacing: descriptorStyle.letterSpacing,
            linkGap: linksStyle.gap,
          };
        }
        """
    )


def test_portfolio_is_deployed_at_site_root(page) -> None:
    open_site_page(page, "index.html")

    expect(page.get_by_role("heading", name="Science enabler.")).to_be_visible()
    expect(page.get_by_role("link", name="Field notes")).to_have_attribute(
        "href", "blog/"
    )
    expect(page.get_by_role("link", name="Download CV")).to_have_attribute(
        "href", "assets/Jakob_Stender_Guldberg_CV.pdf"
    )
    expect(page.locator("link[rel='icon']")).to_have_attribute(
        "href", "assets/goose.png"
    )
    assert (
        page.get_by_label("Primary navigation").get_by_role("link").all_inner_texts()
        == NAV_LABELS
    )
    expect(page.locator(".md-search")).to_have_count(0)


def test_blog_index_uses_portfolio_design_language(page) -> None:
    open_site_page(page, "blog/index.html")

    expect(page.get_by_role("heading", name="Field notes.")).to_be_visible()
    heading_size = page.get_by_role("heading", name="Field notes.").evaluate(
        "element => parseFloat(getComputedStyle(element).fontSize)"
    )
    assert heading_size <= 88
    expect(page.locator(".brand-mark")).to_have_text("JG")
    expect(page.locator(".note-card")).to_have_count(1)
    assert (
        page.get_by_label("Primary navigation").get_by_role("link").all_inner_texts()
        == NAV_LABELS
    )
    expect(
        page.get_by_label("Primary navigation").get_by_role("link", name="Portfolio")
    ).to_have_attribute("href", "/")
    expect(page.locator(".md-search")).to_have_count(1)
    expect(page.locator("#__config")).not_to_contain_text("navigation.instant")
    expect(page.locator("link[rel='icon']")).to_have_attribute(
        "href", "../assets/goose.png"
    )

    tokens = page.evaluate(
        """
        () => {
          const style = getComputedStyle(document.documentElement);
          return {
            accent: style.getPropertyValue('--field-accent').trim(),
            display: style.getPropertyValue('--field-display').trim(),
          };
        }
        """
    )
    assert tokens["accent"]
    assert "Iowan Old Style" in tokens["display"]


def test_blog_portfolio_links_navigate_and_scroll(page, site_url) -> None:
    destinations = [
        ("Portfolio", "", "#top"),
        ("Contact", "#contact", "#contact"),
    ]

    for label, fragment, target in destinations:
        page.goto(f"{site_url}/blog/")
        page.get_by_label("Primary navigation").get_by_role(
            "link", name=label
        ).click()

        expect(page).to_have_url(f"{site_url}/{fragment}")
        expect(page.locator(target)).to_be_in_viewport()


def test_navigation_geometry_matches_between_portfolio_and_blog(page) -> None:
    page.set_viewport_size({"width": 1440, "height": 900})
    open_site_page(page, "index.html")
    portfolio_navigation = navigation_signature(page)

    open_site_page(page, "blog/index.html")
    blog_navigation = navigation_signature(page)

    assert blog_navigation == portfolio_navigation


def test_blog_mobile_navigation_keeps_search_and_menu(page) -> None:
    page.set_viewport_size({"width": 375, "height": 812})
    open_site_page(page, "blog/index.html")

    menu = page.get_by_role("button", name="Menu")
    expect(menu).to_have_attribute("aria-expanded", "false")
    expect(page.locator(".nav-search")).to_be_visible()
    mobile_heading_size = page.get_by_role("heading", name="Field notes.").evaluate(
        "element => parseFloat(getComputedStyle(element).fontSize)"
    )
    assert mobile_heading_size <= 65

    menu.click()
    expect(menu).to_have_attribute("aria-expanded", "true")
    expect(page.get_by_label("Primary navigation")).to_be_visible()


def test_blog_post_keeps_reading_features(page) -> None:
    open_site_page(page, "blog/posts/using-secrets-in-dotenv/index.html")

    expect(
        page.get_by_role(
            "heading", name="Managing secrets in dotenv files with the keyring"
        )
    ).to_be_visible()
    post_heading_size = page.get_by_role(
        "heading", name="Managing secrets in dotenv files with the keyring"
    ).evaluate("element => parseFloat(getComputedStyle(element).fontSize)")
    assert post_heading_size <= 73
    expect(page.locator(".post-meta")).to_contain_text("Field note 001")
    expect(page.locator("pre code").first).to_contain_text("uv tool install keyring")
    expect(page.locator("script[src*='giscus.app/client.js']")).to_have_count(1)
