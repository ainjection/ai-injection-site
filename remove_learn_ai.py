#!/usr/bin/env python3
"""Remove the Learn AI section from the site:
  1. Remove every <a href="../learn-ai/raw.html">...</a> element
  2. Drop the parent <li> wrapper if removing the anchor leaves it empty
  3. Delete the pages/learn-ai/ folder
"""
import re, sys, shutil
from pathlib import Path

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path("C:/Users/clawb/Desktop/claudeclaw-main/site-clones/aishotstudio-full")
PAGES = ROOT / "pages"
LEARN_DIR = PAGES / "learn-ai"

# Match <a ... href="../learn-ai/raw.html" ...>...</a>  (non-greedy across newlines)
ANCHOR_RE = re.compile(
    r'<a\b[^>]*href="\.\./learn-ai/raw\.html"[^>]*>.*?</a>',
    re.IGNORECASE | re.DOTALL,
)
# Empty <li>...</li> after removal — collapse them
EMPTY_LI_RE = re.compile(r'<li[^>]*>\s*</li>', re.IGNORECASE)
# Empty <div>...</div> wrappers with nothing left except whitespace
EMPTY_WRAPPER_RE = re.compile(
    r'<div[^>]*style="text-align:right;"[^>]*>\s*</div>', re.IGNORECASE
)


def strip_page(path: Path) -> tuple[int, int]:
    html = path.read_text(encoding="utf-8", errors="ignore")
    new_html, n_anchor = ANCHOR_RE.subn("", html)
    new_html, n_li = EMPTY_LI_RE.subn("", new_html)
    new_html, n_div = EMPTY_WRAPPER_RE.subn("", new_html)
    if n_anchor or n_li or n_div:
        path.write_text(new_html, encoding="utf-8")
    return n_anchor, n_li + n_div


def main():
    total_a = 0
    total_w = 0
    pages_touched = 0
    for page_dir in sorted(PAGES.iterdir()):
        raw = page_dir / "raw.html"
        if not raw.exists():
            continue
        n_a, n_w = strip_page(raw)
        if n_a or n_w:
            pages_touched += 1
            print(f"  {page_dir.name:42}  removed {n_a} anchor(s), {n_w} empty wrapper(s)")
        total_a += n_a
        total_w += n_w
    print(f"\nTotals: {total_a} learn-ai anchors removed, {total_w} empty wrappers cleaned across {pages_touched} pages")

    if LEARN_DIR.exists():
        shutil.rmtree(LEARN_DIR)
        print(f"Deleted {LEARN_DIR}")
    else:
        print(f"learn-ai folder already gone")


if __name__ == "__main__":
    main()
