#!/usr/bin/env python3
"""Replace AIShotStudio's affiliate redirects with Rob's own affiliate URLs.

Reads affiliate-links.csv (4 cols: slug, tool_name, affiliate_signup_url, your_affiliate_url).
For every row where `your_affiliate_url` is non-empty, replaces every
`https://aishotstudio.com/go/<slug>` and `https://aishotstudio.com/try/<slug>`
across all pages with the user's URL.

Skips rows with blank `your_affiliate_url` (so you can fill them in over time).
Idempotent — re-run any time after editing the CSV.
"""
import csv, re, sys
from pathlib import Path

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path("C:/Users/clawb/Desktop/claudeclaw-main/site-clones/aishotstudio-full")
CSV_PATH = ROOT / "affiliate-links.csv"


def main():
    with open(CSV_PATH, encoding="utf-8-sig") as fp:
        rows = list(csv.DictReader(fp))

    swaps = []
    skipped = []
    for row in rows:
        slug = (row.get("slug") or "").strip()
        new_url = (row.get("your_affiliate_url") or "").strip()
        if not slug:
            continue
        if not new_url:
            skipped.append(slug)
            continue
        swaps.append((slug, new_url))

    if not swaps:
        print("Nothing to swap — fill in the `your_affiliate_url` column in affiliate-links.csv first.")
        if skipped:
            print(f"  ({len(skipped)} rows have no URL yet)")
        return

    print(f"Applying {len(swaps)} affiliate-URL swaps:")
    for slug, url in swaps:
        print(f"  {slug:20} -> {url}")
    print()

    total_replacements = 0
    pages_touched = 0
    for p in (ROOT / "pages").rglob("raw.html"):
        html = p.read_text(encoding="utf-8")
        orig = html
        for slug, new_url in swaps:
            for prefix in ("go", "try"):
                pattern = rf"https://aishotstudio\.com/{prefix}/{re.escape(slug)}(?=[\"'\s>])"
                matches = re.findall(pattern, html)
                if matches:
                    html = re.sub(pattern, new_url.replace("\\", "\\\\"), html)
                    total_replacements += len(matches)
        if html != orig:
            p.write_text(html, encoding="utf-8")
            pages_touched += 1

    print(f"\nReplaced {total_replacements} affiliate URLs across {pages_touched} pages")
    if skipped:
        print(f"\nStill blank (not swapped — left as AIShotStudio's URL): {', '.join(skipped)}")


if __name__ == "__main__":
    main()
