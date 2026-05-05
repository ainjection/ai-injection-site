#!/usr/bin/env python3
"""Site-wide sweep: replace remaining aishotstudio.com references that
rewrite_links.py and the previous email scrub didn't catch.

Rules:
  - mailto:*aishotstudio.com → strip the link, keep inner text
  - aishotstudio.com author/comment/feed/download/category links → href="#"
  - aishotstudio.com root link → ../home/raw.html
  - "AI Shot Studio" / "aiShotStudio" / "AISHOTSTUDIO" brand text → "AI Injection"
"""
import re, sys
from pathlib import Path

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path("C:/Users/clawb/Desktop/claudeclaw-main/site-clones/aishotstudio-full")
PAGES = ROOT / "pages"

# Each tuple: (regex, replacement, label)
RULES = [
    # mailto:*@aishotstudio.com (strip wrapper anchor)
    (re.compile(r'<a[^>]*href="mailto:[^"]*aishotstudio\.com[^"]*"[^>]*>([^<]*)</a>', re.IGNORECASE),
     r'\1', "mailto strip"),
    # plain text email
    (re.compile(r'\b[A-Za-z0-9._%+-]+@aishotstudio\.com\b', re.IGNORECASE),
     '', "email text"),
    # author / author-comments
    (re.compile(r'href="https?://aishotstudio\.com/author/[^"]+"', re.IGNORECASE),
     'href="#"', "author"),
    # comments feed / regular feed / wp-json / xmlrpc
    (re.compile(r'href="https?://aishotstudio\.com/(comments/feed|feed|wp-json|xmlrpc\.php|wp-login\.php)[^"]*"', re.IGNORECASE),
     'href="#"', "feed/api"),
    # download pages
    (re.compile(r'href="https?://aishotstudio\.com/download/[^"]+"', re.IGNORECASE),
     'href="#"', "download"),
    # category / tag pages
    (re.compile(r'href="https?://aishotstudio\.com/(category|tag)/[^"]+"', re.IGNORECASE),
     'href="#"', "category/tag"),
    # legal pages — keep them visible since they exist on the source site
    # privacy/cookie/disclaimer/terms - point to '#' (no local copy yet)
    (re.compile(r'href="https?://aishotstudio\.com/(privacy-policy|cookie-policy|disclaimer|terms-of-service)/?[^"]*"', re.IGNORECASE),
     'href="#"', "legal"),
    # root URL
    (re.compile(r'href="https?://aishotstudio\.com/?"', re.IGNORECASE),
     'href="../home/raw.html"', "root"),
    # arbitrary post-id links
    (re.compile(r'href="https?://aishotstudio\.com/\?p=\d+"', re.IGNORECASE),
     'href="#"', "post-id"),
    # Brand text (case-insensitive: "AIShotStudio", "aiShotStudio", "AISHOTSTUDIO", "AI Shot Studio")
    # ONLY in user-visible text — inside >...< boundaries — so we don't corrupt resource URLs.
    (re.compile(r'(>[^<]*?\b)AI ?Shot ?Studio\b', re.IGNORECASE),
     lambda m: m.group(1) + 'AI Injection', "brand text"),
]


def main():
    totals = {label: 0 for _, _, label in RULES}
    pages_touched = 0
    for page_dir in sorted(PAGES.iterdir()):
        raw = page_dir / "raw.html"
        if not raw.exists():
            continue
        html = raw.read_text(encoding="utf-8", errors="ignore")
        orig = html
        for pat, repl, label in RULES:
            html, n = pat.subn(repl, html)
            totals[label] += n
        if html != orig:
            raw.write_text(html, encoding="utf-8")
            pages_touched += 1
    print(f"Touched {pages_touched} pages\n")
    for label, n in totals.items():
        print(f"  {label:18} {n}")
    print(f"\n=== {sum(totals.values())} total replacements ===")


if __name__ == "__main__":
    main()
