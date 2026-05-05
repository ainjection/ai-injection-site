#!/usr/bin/env python3
"""Render lead-magnet/ai-injection-master-prompt-pack.html to PDF via headless
Chromium (Playwright). Outputs ai-injection-master-prompt-pack.pdf next to it.
"""
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path("C:/Users/clawb/Desktop/claudeclaw-main/site-clones/aishotstudio-full")
HTML = ROOT / "lead-magnet" / "ai-injection-master-prompt-pack.html"
PDF  = ROOT / "lead-magnet" / "ai-injection-master-prompt-pack.pdf"


def main():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        ctx = browser.new_context()
        page = ctx.new_page()
        page.goto(HTML.as_uri(), wait_until="networkidle")
        page.pdf(
            path=str(PDF),
            format="A4",
            print_background=True,
            margin={"top": "0", "right": "0", "bottom": "0", "left": "0"},
        )
        browser.close()
    size_kb = PDF.stat().st_size / 1024
    print(f"Wrote {PDF} ({size_kb:.1f} KB)")


if __name__ == "__main__":
    main()
