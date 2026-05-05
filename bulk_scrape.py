#!/usr/bin/env python3
"""Bulk-scrape AIShotStudio pages via curl + MarkItDown (no Firecrawl credits).

Reads URL list, fetches HTML, converts to markdown, downloads page images.
"""
import json, os, re, subprocess, sys, urllib.request
from pathlib import Path

ROOT = Path("C:/Users/clawb/Desktop/claudeclaw-main/site-clones/aishotstudio-full")
PAGES = ROOT / "pages"

# URLs left to scrape (Tier 2/3/4 minus what Firecrawl already got)
URLS = [
    ("ai-toolset", "https://aishotstudio.com/ai-toolset/"),
    ("learn-ai", "https://aishotstudio.com/learn-ai/"),
    # Tier 3 — specialized prompt pages
    ("still-camera-fix", "https://aishotstudio.com/still-camera-how-to-fix-camera/"),
    ("true-360-180-orbit", "https://aishotstudio.com/true-360-180-degree-camera-orbit/"),
    ("higgsfield-camera-comparison", "https://aishotstudio.com/higgsfield-camera-comparison/"),
    ("higgsfield-focal-length", "https://aishotstudio.com/higgsfield-focal-length-examples/"),
    ("higgsfield-aperture", "https://aishotstudio.com/higgsfield-aperture-examples/"),
    ("16-ai-image-generators", "https://aishotstudio.com/comparison-of-16-ai-image-generators/"),
    ("elevenlabs-audio-tags", "https://aishotstudio.com/elevenlabs-audio-tags-list/"),
    ("technical-portrait-poses", "https://aishotstudio.com/technical-portrait-poses-prompts/"),
    ("gender-swap-prompts", "https://aishotstudio.com/gender-swap-image-and-video-prompts/"),
    ("character-actor-catwalk", "https://aishotstudio.com/character-actor-catwalk/"),
    ("border-break-master", "https://aishotstudio.com/border-break-video-master-prompt/"),
    # Tier 4 — meta-prompts
    ("lacoste-crocodile-seedance", "https://aishotstudio.com/lacoste-crocodile-seedance-2-prompt/"),
    ("morning-rush-seedance", "https://aishotstudio.com/morning-rush-seedance-2-prompt/"),
    ("volleyball-freeze-seedance", "https://aishotstudio.com/volleyball-freeze-frame-seedance-2-prompt/"),
    ("phone-catch-seedance", "https://aishotstudio.com/phone-catch-seedance-2-0-prompt/"),
    ("cockroaches-bed", "https://aishotstudio.com/cockroaches-bed/"),
]

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0 Safari/537.36"


def fetch(url, target):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=60) as r:
        target.write_bytes(r.read())


def html_to_md(html_path, md_path):
    """Convert HTML to Markdown via MarkItDown."""
    try:
        result = subprocess.run(
            ["python", "-m", "markitdown", str(html_path), "-o", str(md_path)],
            capture_output=True, text=True, timeout=60
        )
        return result.returncode == 0
    except Exception as e:
        print(f"  markitdown error: {e}")
        return False


def extract_images(html_text):
    urls = sorted(set(re.findall(
        r'https?://aishotstudio\.com/[^"\s\)\]\']+\.(?:webp|jpg|jpeg|png|svg|gif)(?:\?[^"\s\)\]\']*)?',
        html_text, re.I
    )))
    seen = set()
    unique = []
    for u in urls:
        clean_url = u.split('?')[0]
        if clean_url not in seen:
            seen.add(clean_url)
            unique.append(clean_url)
    return unique


def download_images(urls, out_dir):
    out_dir.mkdir(exist_ok=True, parents=True)
    downloaded = 0
    failed = 0
    for url in urls[:50]:
        fname = os.path.basename(url.split('?')[0])
        target = out_dir / fname
        if target.exists() and target.stat().st_size > 0:
            downloaded += 1
            continue
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=30) as r:
                target.write_bytes(r.read())
            downloaded += 1
        except Exception:
            failed += 1
    return downloaded, failed


def main():
    PAGES.mkdir(parents=True, exist_ok=True)
    summary = []
    for slug, url in URLS:
        page_dir = PAGES / slug
        page_dir.mkdir(parents=True, exist_ok=True)
        html_path = page_dir / "raw.html"
        md_path = page_dir / "page.md"
        try:
            print(f"[{slug}] fetching...")
            fetch(url, html_path)
            html = html_path.read_text(encoding='utf-8', errors='ignore')
            html_to_md(html_path, md_path)
            md_lines = md_path.read_text(encoding='utf-8', errors='ignore').count('\n') if md_path.exists() else 0
            imgs = extract_images(html)
            (page_dir / 'image-urls.json').write_text(json.dumps(imgs, indent=2), encoding='utf-8')
            dl, fail = download_images(imgs, page_dir / 'images')
            print(f"  md: {md_lines} lines | images: {dl} ok / {fail} fail of {len(imgs)} unique")
            summary.append({"slug": slug, "url": url, "status": "ok", "md_lines": md_lines, "images_total": len(imgs), "images_downloaded": dl, "images_failed": fail})
        except Exception as e:
            print(f"  ERROR {slug}: {e}")
            summary.append({"slug": slug, "url": url, "status": "error", "error": str(e)})
    (ROOT / 'bulk_scrape_summary.json').write_text(json.dumps(summary, indent=2), encoding='utf-8')
    ok = sum(1 for s in summary if s.get('status') == 'ok')
    print(f"\n=== {ok}/{len(URLS)} pages scraped ===")


if __name__ == '__main__':
    main()
