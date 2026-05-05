#!/usr/bin/env python3
"""Replace both top-banner spots on every page with a high-conversion lead-magnet
CTA bar that links to /pages/get-the-pack/raw.html (where the MailerLite form lives).

Targets two structures:
  1. The JS rotating banner: <div id="rotating-header-banner"></div> + the
     <script> that fills it with a random image.
  2. The static <img> banner inside an <a href="...skool..."> wrapper used as
     the mobile/medium-viewport hero banner.

Both get replaced with the same CTA HTML so the site visually pushes ONE call to
action above the fold: get the free prompt pack.
"""
import re, sys
from pathlib import Path

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path("C:/Users/clawb/Desktop/claudeclaw-main/site-clones/aishotstudio-full")
PAGES = ROOT / "pages"

CTA_HTML = (
    '<a href="../get-the-pack/raw.html" class="aii-hero-cta-banner" '
    'style="display:flex;align-items:center;justify-content:center;gap:14px;'
    'width:100%;max-width:850px;height:120px;padding:0 28px;'
    'background:linear-gradient(135deg,#0F0F23 0%,#1a1140 50%,#2a0f5e 100%);'
    'border-radius:8px;text-decoration:none;color:#FFFFFF;'
    'box-shadow:0 0 30px rgba(0,212,255,0.35),inset 0 0 60px rgba(139,92,246,0.18);'
    'border:1px solid rgba(0,212,255,0.45);'
    'font-family:Inter,-apple-system,BlinkMacSystemFont,sans-serif;'
    'transition:transform .15s ease,box-shadow .15s ease;'
    'position:relative;overflow:hidden;">'
    '<div style="display:flex;flex-direction:column;flex:1 1 auto;line-height:1.2;">'
    '<div style="font-size:11px;font-weight:800;letter-spacing:0.25em;color:#00D4FF;text-transform:uppercase;margin-bottom:6px;">📥 Free download · No credit card</div>'
    '<div style="font-size:22px;font-weight:900;color:#fff;letter-spacing:-0.01em;">Get the AI Injection Master Prompt Pack</div>'
    '<div style="font-size:13px;color:#a8a8c0;margin-top:4px;">200+ AI prompts · camera moves · lighting · shots · music · transitions</div>'
    '</div>'
    '<span style="display:inline-flex;align-items:center;gap:6px;'
    'padding:12px 24px;border-radius:28px;'
    'background:linear-gradient(135deg,#00D4FF 0%,#8B5CF6 100%);'
    'color:#0F0F23;font-weight:800;font-size:14px;white-space:nowrap;'
    'box-shadow:0 0 20px rgba(0,212,255,0.5);flex:0 0 auto;">'
    'Get it free →</span>'
    '</a>'
)

# (1) Replace the rotating-header-banner div + its <script> block
ROTATING_RE = re.compile(
    r'<div id="rotating-header-banner"></div>\s*<script>.*?</script>',
    re.IGNORECASE | re.DOTALL,
)

# (2) Replace the static <a href="...skool..."><img ...AI-Injection-Banner..."></a>
STATIC_RE = re.compile(
    r'<a class="fusion-no-lightbox"[^>]*href="https://www\.skool\.com/ai-injection-4241"[^>]*>'
    r'<img[^>]*AI-Injection-Banner[^>]*></a>',
    re.IGNORECASE,
)


def fix_page(path: Path) -> tuple[int, int]:
    html = path.read_text(encoding="utf-8", errors="ignore")
    new_html, n_rot = ROTATING_RE.subn(CTA_HTML, html)
    new_html, n_static = STATIC_RE.subn(CTA_HTML, new_html)
    if n_rot or n_static:
        path.write_text(new_html, encoding="utf-8")
    return n_rot, n_static


def main():
    total_rot = 0
    total_static = 0
    pages_touched = 0
    for page_dir in sorted(PAGES.iterdir()):
        raw = page_dir / "raw.html"
        if not raw.exists():
            continue
        # Skip the lead-magnet page itself
        if page_dir.name == "get-the-pack":
            continue
        n_rot, n_static = fix_page(raw)
        if n_rot or n_static:
            pages_touched += 1
            print(f"  {page_dir.name:42} rotating={n_rot}  static={n_static}")
        total_rot += n_rot
        total_static += n_static
    print(f"\n=== {pages_touched} pages updated · rotating banners replaced: {total_rot} · static banners replaced: {total_static} ===")


if __name__ == "__main__":
    main()
