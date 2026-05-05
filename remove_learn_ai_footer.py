#!/usr/bin/env python3
"""Remove the footer 'Learn AI' column from every page.

The footer has 3 sibling fusion-layout-column divs (AI INJECTION, Learn AI,
AI Toolset). The Learn AI one always contains an <h4>Learn AI</h4> heading.
Find that div and remove it as a unit.
"""
import re, sys
from pathlib import Path

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path("C:/Users/clawb/Desktop/claudeclaw-main/site-clones/aishotstudio-full")
PAGES = ROOT / "pages"


def find_matching_div_end(html: str, start: int) -> int:
    """Return the index just past the </div> matching the opening <div at start."""
    depth = 0
    i = start
    n = len(html)
    while i < n:
        if html[i] == "<":
            if html[i:i+5].lower() == "<div ":
                depth += 1
                i += 5
                continue
            if html[i:i+5].lower() == "<div>":
                depth += 1
                i += 5
                continue
            if html[i:i+6].lower() == "</div>":
                depth -= 1
                i += 6
                if depth == 0:
                    return i
                continue
        i += 1
    return -1


COLUMN_RE = re.compile(r'<div class="fusion-layout-column fusion_builder_column ', re.IGNORECASE)
LEARN_AI_HEADING = re.compile(r'<h4[^>]*>Learn AI</h4>', re.IGNORECASE)


def strip_footer(path: Path) -> int:
    html = path.read_text(encoding="utf-8", errors="ignore")
    out = []
    i = 0
    removed = 0
    while True:
        m = COLUMN_RE.search(html, i)
        if not m:
            out.append(html[i:])
            break
        col_start = m.start()
        col_end = find_matching_div_end(html, col_start)
        if col_end < 0:
            out.append(html[i:])
            break
        block = html[col_start:col_end]
        if LEARN_AI_HEADING.search(block):
            out.append(html[i:col_start])
            removed += 1
        else:
            out.append(html[i:col_end])
        i = col_end
    if removed:
        path.write_text("".join(out), encoding="utf-8")
    return removed


def main():
    total = 0
    for page_dir in sorted(PAGES.iterdir()):
        raw = page_dir / "raw.html"
        if not raw.exists():
            continue
        n = strip_footer(raw)
        if n:
            print(f"  {page_dir.name:42}  removed {n} footer Learn AI column(s)")
        total += n
    print(f"\n=== {total} footer Learn AI columns removed ===")


if __name__ == "__main__":
    main()
