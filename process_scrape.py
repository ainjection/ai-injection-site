#!/usr/bin/env python3
"""Process a saved Firecrawl scrape result file: extract markdown, raw HTML, screenshot URL, and image URLs.

Usage: python process_scrape.py <tool_results_file> <output_slug>
Example: python process_scrape.py /path/to/result.txt 42-camera-movements
"""
import json, re, sys, urllib.request, os
from pathlib import Path

def main():
    if len(sys.argv) < 3:
        print("usage: process_scrape.py <input_json> <output_slug>")
        sys.exit(1)

    src = sys.argv[1]
    slug = sys.argv[2]

    out_dir = Path("C:/Users/clawb/Desktop/claudeclaw-main/site-clones/aishotstudio-full/pages") / slug
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "images").mkdir(exist_ok=True)

    # Parse the tool-result wrapper
    with open(src, 'r', encoding='utf-8') as f:
        arr = json.load(f)
    data = json.loads(arr[0]['text'])

    # Save markdown
    if 'markdown' in data:
        (out_dir / 'page.md').write_text(data['markdown'], encoding='utf-8')
        print(f"  markdown: {len(data['markdown'])} chars")

    # Save raw HTML
    if 'rawHtml' in data:
        (out_dir / 'raw.html').write_text(data['rawHtml'], encoding='utf-8')

    if 'html' in data:
        (out_dir / 'clean.html').write_text(data['html'], encoding='utf-8')

    # Save metadata
    if 'metadata' in data:
        (out_dir / 'metadata.json').write_text(json.dumps(data['metadata'], indent=2, default=str), encoding='utf-8')

    # Download screenshot
    if 'screenshot' in data and data['screenshot']:
        try:
            req = urllib.request.Request(data['screenshot'], headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=60) as r:
                (out_dir / 'screenshot.png').write_bytes(r.read())
            print(f"  screenshot: saved")
        except Exception as e:
            print(f"  screenshot ERROR: {e}")

    # Extract all image URLs from raw HTML
    raw = data.get('rawHtml', '') + data.get('html', '') + data.get('markdown', '')
    img_urls = sorted(set(re.findall(r'https?://aishotstudio\.com/[^"\s\)\]]+\.(?:webp|jpg|jpeg|png|svg|gif)(?:\?[^"\s\)\]]*)?', raw, re.I)))
    # Strip query strings for the saved filename, dedupe
    seen = set()
    unique = []
    for u in img_urls:
        clean_url = u.split('?')[0]
        if clean_url not in seen:
            seen.add(clean_url)
            unique.append(clean_url)
    img_urls = unique

    print(f"  found {len(img_urls)} unique images")
    (out_dir / 'image-urls.json').write_text(json.dumps(img_urls, indent=2), encoding='utf-8')

    # Bulk download images (cap at 100 to avoid runaway)
    downloaded = 0
    for i, url in enumerate(img_urls[:100]):
        fname = os.path.basename(url.split('?')[0])
        target = out_dir / 'images' / fname
        if target.exists():
            downloaded += 1
            continue
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=30) as r:
                target.write_bytes(r.read())
            downloaded += 1
        except Exception as e:
            print(f"  img {i+1} ERROR: {url} :: {e}")

    print(f"  downloaded {downloaded}/{len(img_urls)} images")
    print(f"  output: {out_dir}")

if __name__ == '__main__':
    main()
