#!/usr/bin/env python3
"""Inject a sticky Skool CTA bar at the top of every page.

The bar is fixed-position, full-width, AI Injection branded (cyan/purple
gradient with neon glow), persists on scroll, and links to Rob's Skool
community.
"""
import re, sys
from pathlib import Path

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path("C:/Users/clawb/Desktop/claudeclaw-main/site-clones/aishotstudio-full")
PAGES = ROOT / "pages"
SKOOL_URL = "https://www.skool.com/ai-injection-4241"

# Marker comment so we can detect (and replace) prior injections idempotently.
MARKER = "<!-- AI INJECTION SKOOL CTA -->"

CTA_HTML = f"""{MARKER}
<style id="aii-skool-cta-style">
  body {{ padding-top: 56px !important; }}
  #aii-skool-cta {{
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    z-index: 999999;
    height: 56px;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 14px;
    padding: 0 24px;
    background: linear-gradient(90deg, #0F0F23 0%, #1a1140 50%, #0F0F23 100%);
    border-bottom: 1px solid rgba(0, 212, 255, 0.4);
    box-shadow: 0 2px 30px rgba(0, 212, 255, 0.25);
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    color: #FFFFFF;
    overflow: hidden;
  }}
  #aii-skool-cta::before {{
    content: '';
    position: absolute;
    inset: 0;
    background: radial-gradient(ellipse at center, rgba(0,212,255,0.15) 0%, transparent 70%);
    pointer-events: none;
  }}
  #aii-skool-cta .aii-cta-text {{
    font-size: 14px;
    font-weight: 600;
    letter-spacing: 0.01em;
    z-index: 1;
  }}
  #aii-skool-cta .aii-cta-pulse {{
    display: inline-block;
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background: #00D4FF;
    box-shadow: 0 0 10px #00D4FF, 0 0 20px #00D4FF;
    margin-right: 10px;
    animation: aii-pulse 1.6s ease-in-out infinite;
    vertical-align: middle;
  }}
  @keyframes aii-pulse {{
    0%, 100% {{ opacity: 1; transform: scale(1); }}
    50% {{ opacity: 0.5; transform: scale(1.4); }}
  }}
  #aii-skool-cta .aii-cta-button {{
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 8px 16px;
    background: linear-gradient(135deg, #00D4FF 0%, #8B5CF6 100%);
    color: #0F0F23 !important;
    font-weight: 800;
    font-size: 13px;
    border-radius: 24px;
    text-decoration: none;
    box-shadow: 0 0 20px rgba(0, 212, 255, 0.5);
    transition: transform 0.15s ease, box-shadow 0.15s ease;
    z-index: 1;
    white-space: nowrap;
  }}
  #aii-skool-cta .aii-cta-button.ghost {{
    background: transparent;
    color: #FFFFFF !important;
    border: 1px solid rgba(0,212,255,0.55);
    box-shadow: none;
  }}
  #aii-skool-cta .aii-cta-button:hover {{
    transform: translateY(-1px) scale(1.04);
    box-shadow: 0 0 30px rgba(0, 212, 255, 0.8);
  }}
  #aii-skool-cta .aii-cta-button.ghost:hover {{
    background: rgba(0,212,255,0.1);
    box-shadow: 0 0 16px rgba(0,212,255,0.3);
  }}
  @media (max-width: 720px) {{
    #aii-skool-cta {{ padding: 0 10px; gap: 8px; }}
    #aii-skool-cta .aii-cta-text {{ display: none; }}
    #aii-skool-cta .aii-cta-button {{ padding: 6px 12px; font-size: 12px; }}
    body {{ padding-top: 56px !important; }}
  }}
</style>
<div id="aii-skool-cta" role="banner">
  <span class="aii-cta-text"><span class="aii-cta-pulse"></span>Free download + community for AI creators</span>
  <a class="aii-cta-button" href="/pages/get-the-pack/raw.html">📥 Get the Free Prompt Pack</a>
  <a class="aii-cta-button ghost" href="{SKOOL_URL}" target="_blank" rel="noopener noreferrer">Join Skool</a>
</div>
"""

# Match an opening <body ...>  tag (with attributes), capturing it for replacement
BODY_RE = re.compile(r'(<body\b[^>]*>)', re.IGNORECASE)
EXISTING_RE = re.compile(re.escape(MARKER) + r'.*?</div>\s*', re.IGNORECASE | re.DOTALL)


def inject(path: Path) -> str:
    html = path.read_text(encoding="utf-8", errors="ignore")
    # Remove any existing injection so we can re-run idempotently.
    html = EXISTING_RE.sub("", html)
    new_html, n = BODY_RE.subn(lambda m: m.group(1) + "\n" + CTA_HTML, html, count=1)
    if n:
        path.write_text(new_html, encoding="utf-8")
        return "injected"
    return "no <body> tag"


def main():
    counts = {"injected": 0, "no <body> tag": 0}
    for page_dir in sorted(PAGES.iterdir()):
        raw = page_dir / "raw.html"
        if not raw.exists():
            continue
        result = inject(raw)
        counts[result] = counts.get(result, 0) + 1
    print(f"Pages injected: {counts['injected']}")
    if counts.get("no <body> tag", 0):
        print(f"Pages without <body>: {counts['no <body> tag']}")


if __name__ == "__main__":
    main()
