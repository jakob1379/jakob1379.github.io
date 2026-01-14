#!/usr/bin/env python3
"""
Minify HTML, CSS, and JavaScript files in the built site directory using minify-html.
"""

import os
import sys
from pathlib import Path

try:
    import minify_html
except ImportError:
    print("Error: minify-html not installed. Run: uv add minify-html")
    sys.exit(1)


def minify_file(content: str, file_path: Path) -> str:
    """Minify content based on file type."""
    # minify-html can minify HTML, JS, and CSS
    # We'll let it detect based on content, but we can also pass minify_js=True, minify_css=True
    # For HTML files, we want to minify JS and CSS embedded as well.
    # For standalone JS/CSS files, we can still use minify_html.minify with appropriate flags.
    if file_path.suffix == ".html":
        return minify_html.minify(
            content,
            minify_js=True,
            minify_css=True,
            keep_comments=False,
        )
    elif file_path.suffix == ".js":
        # Minify JavaScript
        return minify_html.minify(
            content,
            minify_js=True,
            minify_css=False,
            keep_comments=False,
        )
    elif file_path.suffix == ".css":
        # Minify CSS
        return minify_html.minify(
            content,
            minify_js=False,
            minify_css=True,
            keep_comments=False,
        )
    else:
        return content


def process_file(file_path: Path) -> None:
    """Minify a single file in-place."""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        original_size = len(content)
        minified = minify_file(content, file_path)

        # Only write if minification actually reduced size
        if len(minified) < original_size:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(minified)
            reduction = original_size - len(minified)
            print(f"✓ {file_path.relative_to(SITE_DIR)}: {original_size} → {len(minified)} bytes (-{reduction})")
        else:
            print(f"○ {file_path.relative_to(SITE_DIR)}: no reduction ({original_size} bytes)")

    except Exception as e:
        print(f"✗ {file_path.relative_to(SITE_DIR)}: {e}")
        # Don't fail the whole process on a single file error


def main() -> None:
    """Main entry point."""
    global SITE_DIR
    SITE_DIR = Path.cwd() / "site"
    
    if not SITE_DIR.exists():
        print(f"Error: Site directory not found at {SITE_DIR}")
        print("Run 'zensical build' first.")
        sys.exit(1)

    print(f"Minifying files in {SITE_DIR}")

    # File extensions to process
    html_files = list(SITE_DIR.rglob("*.html"))
    css_files = list(SITE_DIR.rglob("*.css"))
    js_files = list(SITE_DIR.rglob("*.js"))

    total_files = len(html_files) + len(css_files) + len(js_files)
    print(f"Found {len(html_files)} HTML, {len(css_files)} CSS, {len(js_files)} JS files")

    for file in html_files + css_files + js_files:
        process_file(file)

    print("Minification complete.")


if __name__ == "__main__":
    main()
