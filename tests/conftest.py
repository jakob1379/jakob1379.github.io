"""
Playwright pytest configuration for cross-browser testing and device emulation.
This extends the pytest-playwright plugin with custom viewport options.
"""

import pytest
from typing import Optional, Tuple


def pytest_addoption(parser):
    """Add custom command-line options for viewport configuration."""
    parser.addoption(
        "--viewport",
        default=None,
        help="Custom viewport size in format 'widthxheight' (e.g., '375x667').",
    )


@pytest.fixture(scope="session")
def viewport_size(pytestconfig) -> Optional[Tuple[int, int]]:
    """Parse and return custom viewport dimensions."""
    viewport = pytestconfig.getoption("--viewport")
    if viewport:
        try:
            width, height = map(int, viewport.split("x"))
            return width, height
        except ValueError:
            pass
    return None


@pytest.fixture(scope="session")
def browser_context_args(
    request,
    playwright,
    device,
    viewport_size,
):
    """
    Extend browser context with device emulation and custom viewport.

    This fixture merges device configuration (if provided via --device) and
    custom viewport size (if provided via --viewport) into the browser context.
    """
    # Get the original browser_context_args from plugin
    original = request.getfixturevalue("browser_context_args")
    context = {**original}

    # Apply device emulation if specified (device fixture provided by plugin)
    # Note: plugin already merges device, but we ensure viewport override
    # Override viewport if custom viewport is specified
    if viewport_size:
        width, height = viewport_size
        context["viewport"] = {"width": width, "height": height}

    return context


# Marker for browser-specific tests
def pytest_configure(config):
    config.addinivalue_line(
        "markers",
        "browser(name): mark test to run only on specific browser (chromium, firefox, webkit)",
    )


# Optional fixture for mobile device emulation (if not using --device)
@pytest.fixture
def mobile_context(playwright):
    """Provide a mobile device configuration (iPhone 12)."""
    return playwright.devices.get("iPhone 12", {})
