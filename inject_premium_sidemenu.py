#!/usr/bin/env python3
"""Inject a 'Premium' item into the side / off-canvas menu of every page,
right AFTER the Home menu item, with cyan/purple gradient highlight so it pops.
Idempotent via marker comment.
"""
import re, sys
from pathlib import Path

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path("C:/Users/clawb/Desktop/claudeclaw-main/site-clones/aishotstudio-full")
PAGES = ROOT / "pages"
SKIP = {"premium", "get-the-pack"}

MARKER = "<!--AII-PREMIUM-SIDEMENU-->"
PREMIUM_ITEM = (
    f'{MARKER}'
    '<li id="menu-item-aii-premium" '
    'class="menu-item menu-item-type-post_type menu-item-object-page awb-menu__li awb-menu__main-li awb-menu__main-li_regular" '
    'style="background:linear-gradient(135deg,rgba(139,92,246,0.18) 0%,rgba(0,212,255,0.18) 100%);'
    'border-left:3px solid #00D4FF;'
    'box-shadow:inset 0 0 30px rgba(0,212,255,0.08);">'
    '<a href="../premium/raw.html" '
    'class="awb-menu__main-a awb-menu__main-a_regular" '
    'style="color:#fff !important;font-weight:800 !important;">'
    '<span class="menu-text" '
    'style="background:linear-gradient(135deg,#00D4FF,#8B5CF6);'
    '-webkit-background-clip:text;background-clip:text;color:transparent !important;'
    'font-weight:900;">⚡ Premium Tools</span>'
    '</a></li>'
)

# Find the Home <li>...</li> close and inject after it.
HOME_LI_CLOSE_RE = re.compile(
    r'(<a href="\.\./home/raw\.html"[^>]*class="awb-menu__main-a[^"]*"[^>]*>'
    r'<span class="menu-text">Home</span></a></li>)',
    re.IGNORECASE,
)
EXISTING_RE = re.compile(re.escape(MARKER) + r'.*?</li>', re.IGNORECASE | re.DOTALL)


def inject(path: Path) -> int:
    html = path.read_text(encoding="utf-8", errors="ignore")
    html = EXISTING_RE.sub("", html)
    new_html, n = HOME_LI_CLOSE_RE.subn(lambda m: m.group(1) + PREMIUM_ITEM, html)
    if n:
        path.write_text(new_html, encoding="utf-8")
    return n


def main():
    total = 0
    pages = 0
    for page_dir in sorted(PAGES.iterdir()):
        raw = page_dir / "raw.html"
        if not raw.exists():
            continue
        if page_dir.name in SKIP:
            continue
        n = inject(raw)
        if n:
            pages += 1
        total += n
    print(f"Injected Premium side-menu item on {pages} pages ({total} occurrences).")


if __name__ == "__main__":
    main()
