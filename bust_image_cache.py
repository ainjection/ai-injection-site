#!/usr/bin/env python3
"""Append (or refresh) a cache-busting `?v=<timestamp>` query string on every
local image URL in raw.html files.

Properly handles:
  - URLs with no query string         → appends ?v=<ts>
  - URLs already carrying ?v=<digits> → swaps the digits for new timestamp
  - URLs carrying other query params  → merges/replaces the v= key, keeping the rest
"""
import re, sys, time
from pathlib import Path
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path("C:/Users/clawb/Desktop/claudeclaw-main/site-clones/aishotstudio-full")
PAGES = ROOT / "pages"

VERSION = time.strftime("%Y%m%d%H%M")

# Match the URL inside an attribute, including any existing query string.
URL_RE = re.compile(
    r'(images/[A-Za-z0-9._/-]+\.(?:webp|png|jpg|jpeg|svg|ico|gif))(\?[^"\'\s>]*)?',
    re.IGNORECASE,
)


def replace_v(url: str, query: str | None, version: str) -> str:
    """Return url with v=<version>, replacing/merging any prior query params."""
    if not query:
        return f"{url}?v={version}"
    # parse_qsl handles ?a=1&b=2 form; keep_blank_values for safety
    parts = [(k, v) for k, v in parse_qsl(query[1:], keep_blank_values=True) if k != "v"]
    parts.append(("v", version))
    return f"{url}?{urlencode(parts)}"


def rewrite(path: Path) -> int:
    html = path.read_text(encoding="utf-8", errors="ignore")
    new_html, n = URL_RE.subn(lambda m: replace_v(m.group(1), m.group(2), VERSION), html)
    if n and new_html != html:
        path.write_text(new_html, encoding="utf-8")
    return n


def main():
    total = 0
    for page_dir in sorted(PAGES.iterdir()):
        raw = page_dir / "raw.html"
        if not raw.exists():
            continue
        n = rewrite(raw)
        if n:
            print(f"  {page_dir.name:45} {n:3} URLs cache-busted")
        total += n
    print(f"\n=== {total} image URLs got ?v={VERSION} ===")


if __name__ == "__main__":
    main()
