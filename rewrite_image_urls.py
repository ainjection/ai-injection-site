#!/usr/bin/env python3
"""Rewrite aishotstudio.com image URLs in raw.html files to local paths.

Each page directory (pages/<slug>/) has an images/ subfolder containing the
original aishotstudio.com assets we cloned. The HTML still references the live
aishotstudio.com URLs. This script swaps any URL of the form

    https://aishotstudio.com/wp-content/uploads/<YYYY>/<MM>/<file>

to a local path of the form

    images/<file>

ONLY when a matching file exists in pages/<slug>/images/. CSS and JS hosted
under wp-content/uploads/fusion-styles/ and fusion-scripts/ are left alone.
"""
import re, sys
from pathlib import Path

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path("C:/Users/clawb/Desktop/claudeclaw-main/site-clones/aishotstudio-full")
PAGES = ROOT / "pages"

URL_RE = re.compile(
    r'https?://aishotstudio\.com/wp-content/uploads/\d{4}/\d{2}/([^"\'\s)>]+\.(?:webp|png|jpg|jpeg|gif|svg|ico))',
    re.IGNORECASE,
)


def rewrite_page(page_dir: Path) -> tuple[int, int]:
    raw = page_dir / "raw.html"
    images_dir = page_dir / "images"
    if not raw.exists() or not images_dir.exists():
        return (0, 0)

    local_files = {p.name for p in images_dir.iterdir() if p.is_file()}
    html = raw.read_text(encoding="utf-8", errors="ignore")

    swapped = 0
    skipped = 0

    def repl(m):
        nonlocal swapped, skipped
        filename = m.group(1)
        if filename in local_files:
            swapped += 1
            return f"images/{filename}"
        skipped += 1
        return m.group(0)

    new_html = URL_RE.sub(repl, html)
    if swapped:
        raw.write_text(new_html, encoding="utf-8")
    return (swapped, skipped)


def main():
    total_swapped = 0
    total_skipped = 0
    for page_dir in sorted(PAGES.iterdir()):
        if not page_dir.is_dir():
            continue
        s, k = rewrite_page(page_dir)
        if s or k:
            print(f"  {page_dir.name:45} swapped={s:3}  skipped(no local file)={k}")
        total_swapped += s
        total_skipped += k
    print()
    print(f"=== {total_swapped} URLs rewritten to local, {total_skipped} left as remote (no local file) ===")


if __name__ == "__main__":
    main()
