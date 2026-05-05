#!/usr/bin/env python3
"""Install the AI Injection banner: download generated PNG, resize to banner
dimensions, and overwrite the Pippit-Marketing-Reels references in the page.
"""
import sys, urllib.request, re
from pathlib import Path
from io import BytesIO
from PIL import Image

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path("C:/Users/clawb/Desktop/claudeclaw-main/site-clones/aishotstudio-full")
PAGES = ROOT / "pages"

BANNER_URL = "https://d8j0ntlcm91z4.cloudfront.net/user_2x9Q7xsTJdAXnAoIDAoWEOIPy6b/hf_20260504_074558_9f5e57de-139f-40b0-94e2-ad483416b5a6.png"
SIZES = [(850, 120), (200, 28), (400, 56), (600, 85), (800, 113)]
NEW_LINK = "https://www.skool.com/ai-injection-4241"


def download(url: str) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read()


def install_images():
    """Save the banner as AI-Injection-Banner-*.webp in every page's images/ folder
    that has any local images, so the URL rewriter can pick it up.
    """
    print("Downloading banner...")
    png = download(BANNER_URL)
    src = Image.open(BytesIO(png)).convert("RGB")

    # Crop center horizontally to a 7.08:1 aspect (matches 850x120) before resize,
    # so the resize doesn't squish the visual.
    target_aspect = 850 / 120
    sw, sh = src.size
    src_aspect = sw / sh
    if src_aspect > target_aspect:
        # too wide → crop sides
        new_w = int(sh * target_aspect)
        x0 = (sw - new_w) // 2
        cropped = src.crop((x0, 0, x0 + new_w, sh))
    else:
        # too tall → crop top/bottom
        new_h = int(sw / target_aspect)
        y0 = (sh - new_h) // 2
        cropped = src.crop((0, y0, sw, y0 + new_h))

    written = 0
    for page_dir in sorted(PAGES.iterdir()):
        images = page_dir / "images"
        if not (images.exists() and any(images.iterdir())):
            continue
        for w, h in SIZES:
            name = "AI-Injection-Banner.webp" if (w, h) == (850, 120) else f"AI-Injection-Banner-{w}x{h}.webp"
            cropped.resize((w, h), Image.LANCZOS).save(images / name, "WEBP", quality=92, method=6)
            written += 1
    print(f"Wrote {written} banner files across all page image folders\n")


def rewrite_html():
    """Swap Pippit-Marketing-Reels references to AI-Injection-Banner in every
    raw.html. Also update the rotating-banner JS link to the AI Injection Skool
    community.
    """
    # Filename swap: only catch the exact Pippit-Marketing-Reels asset name, anchored to a
    # path-friendly boundary so we don't accidentally rewrite unrelated body text.
    pattern = re.compile(r'(?<![A-Za-z0-9])Pippit-Marketing-Reels(?![A-Za-z0-9])')

    # Banner-context link rewrites: any reference to pippit.com on a banner element.
    # Two forms exist on the cloned page:
    #   1. The rotating-banner JS array:  link: "https://pippit.com"
    #   2. The static <a> wrapping the imageframe:  href="https://pippit.com" (was originally
    #      /go/pippit; my earlier strip_affiliate_links rewrite turned it into pippit.com).
    JS_LINK = re.compile(r'link:\s*"https?://(?:www\.)?pippit\.com/?"', re.IGNORECASE)
    HREF_LINK = re.compile(r'href="https?://(?:www\.)?pippit\.com/?"', re.IGNORECASE)

    total_img = 0
    total_link = 0
    for page_dir in sorted(PAGES.iterdir()):
        raw = page_dir / "raw.html"
        if not raw.exists():
            continue
        html = raw.read_text(encoding="utf-8", errors="ignore")
        new_html, n_img = pattern.subn("AI-Injection-Banner", html)
        new_html, n_js = JS_LINK.subn(f'link: "{NEW_LINK}"', new_html)
        new_html, n_href = HREF_LINK.subn(f'href="{NEW_LINK}"', new_html)
        n_link = n_js + n_href
        if n_img or n_link:
            raw.write_text(new_html, encoding="utf-8")
            print(f"  {page_dir.name:45} banner refs={n_img:2}  link rewrites={n_link}")
        total_img += n_img
        total_link += n_link
    print(f"\n=== {total_img} banner image refs, {total_link} banner link rewrites ===")


def main():
    install_images()
    rewrite_html()


if __name__ == "__main__":
    main()
