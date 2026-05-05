#!/usr/bin/env python3
"""Rebrand the captured AIShotStudio site to AI Injection.

Does two things to every raw.html:
1. Injects a CSS override <style> block right before </head> that:
   - Maps the magenta accent (#d344fa) to AI Injection cyan (#00D4FF)
   - Adds gradient/glow effects on accents
   - Imports Inter font, swaps Heebo/body fonts
   - Hides the original logo image and injects an "AI INJECTION" wordmark
   - Tweaks bg + headings to AI Injection palette
2. Replaces visible AIShotStudio brand text with AI Injection (preserving URLs / asset paths).
"""
import re
from pathlib import Path

ROOT = Path("C:/Users/clawb/Desktop/claudeclaw-main/site-clones/aishotstudio-full")
PAGES = ROOT / "pages"

# AI Injection brand tokens (from ai-injection.vercel.app)
AI_INJECTION_CSS = """
<!-- AI INJECTION REBRAND OVERRIDE -->
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap" rel="stylesheet">
<style id="ai-injection-rebrand">
:root {
  --aii-primary: #00D4FF;
  --aii-secondary: #8B5CF6;
  --aii-bg: #0F0F23;
  --aii-bg-light: #1a1a35;
  --aii-text: #FFFFFF;
  --aii-text-muted: #a0a0b0;
  --aii-glow: rgba(0, 212, 255, 0.5);
  --aii-glow-purple: rgba(139, 92, 246, 0.5);
}

/* Body background + base font */
html, body, .fusion-body {
  background: var(--aii-bg) !important;
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
}

/* Body text default */
body, p, li, span:not([style*="color"]):not([class*="fusion-meta"]) {
  color: var(--aii-text) !important;
}

/* Headings — Inter, white */
h1, h2, h3, h4, h5, h6,
.fusion-title-heading,
[class*="title-heading"] {
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
  color: var(--aii-text) !important;
  letter-spacing: -0.01em;
}

/* Replace any element using the magenta accent color */
[style*="#d344fa" i], [style*="#D344FA"],
[style*="rgb(211, 68, 250)"], [style*="rgb(211,68,250)"],
.fusion-button.button-default,
.button-default,
[class*="awb-color3"],
[class*="awb-color5"] {
  color: var(--aii-primary) !important;
  border-color: var(--aii-primary) !important;
}

/* Magenta backgrounds → cyan-purple gradient */
[style*="background:#d344fa" i], [style*="background-color:#d344fa" i],
[style*="background: #D344FA"], [style*="background-color: #D344FA"],
.fusion-button.button-default[class*="hover"]:hover,
.button-default:hover {
  background: linear-gradient(135deg, var(--aii-primary), var(--aii-secondary)) !important;
  color: #fff !important;
  box-shadow: 0 0 30px var(--aii-glow);
}

/* The + plus icon buttons on the home page card grid (originally magenta squares) */
.fusion-button-icon-divider,
.fusion-imageframe a,
[class*="hover-type-zoomin"] a {
  border-color: var(--aii-primary) !important;
}
.fusion-imageframe::after,
.fusion-imageframe a::after {
  background: linear-gradient(135deg, var(--aii-primary), var(--aii-secondary)) !important;
}

/* Card backgrounds */
.fusion-column-wrapper,
.fusion-column,
[class*="awb-card"],
.fusion-content-boxes-1 .content-box-wrapper,
.fusion-flip-box,
.fusion-flip-boxes .flip-box-wrapper {
  background: var(--aii-bg-light) !important;
  border-color: rgba(0, 212, 255, 0.15) !important;
}

/* Top header */
.fusion-header,
.fusion-header-wrapper,
header,
.fusion-secondary-header,
.fusion-flyout-menu-icons,
.fusion-mobile-menu,
.fusion-flyout-menu,
[class*="awb-flyout-menu"] {
  background: var(--aii-bg) !important;
  border-color: rgba(0, 212, 255, 0.2) !important;
}

/* Footer */
.fusion-footer,
.fusion-footer-widget-area,
.fusion-footer-copyright-area {
  background: #08081a !important;
  border-top: 1px solid rgba(0, 212, 255, 0.2) !important;
}

/* Links */
a:not(.fusion-button):not([class*="awb-no-style"]),
.fusion-text a {
  color: var(--aii-primary) !important;
}
a:hover { color: var(--aii-secondary) !important; }

/* HIDE the original AIShotStudio logo images, inject AI INJECTION wordmark in their place */
img[src*="logo.webp" i],
img[src*="logo.png" i],
img[src*="logo-footer.webp" i] {
  display: none !important;
}
/* Target the link wrapper that directly holds the logo image — render wordmark via ::before. Use single selector to avoid duplicate rendering. */
a.fusion-no-lightbox:has(> img[src*="logo"]) {
  display: inline-flex !important;
  align-items: center;
  min-height: 50px;
  padding: 0 4px;
}
a.fusion-no-lightbox:has(> img[src*="logo"])::before {
  content: "AI INJECTION";
  font-family: 'Inter', -apple-system, sans-serif;
  font-weight: 900;
  font-size: 32px;
  letter-spacing: -0.025em;
  line-height: 1;
  background: linear-gradient(135deg, var(--aii-primary) 0%, var(--aii-secondary) 100%);
  -webkit-background-clip: text;
  background-clip: text;
  -webkit-text-fill-color: transparent;
  color: var(--aii-primary);
  filter: drop-shadow(0 0 14px var(--aii-glow));
  white-space: nowrap;
}
/* Footer uses <span> wrapper instead of <a> */
span.fusion-imageframe:has(> img[src*="logo-footer"])::before {
  content: "AI INJECTION";
  display: inline-flex;
  align-items: center;
  font-family: 'Inter', -apple-system, sans-serif;
  font-weight: 900;
  font-size: 24px;
  letter-spacing: -0.02em;
  line-height: 1;
  background: linear-gradient(135deg, var(--aii-primary) 0%, var(--aii-secondary) 100%);
  -webkit-background-clip: text;
  background-clip: text;
  -webkit-text-fill-color: transparent;
  color: var(--aii-primary);
  filter: drop-shadow(0 0 10px var(--aii-glow));
  white-space: nowrap;
}

/* Hover/glow on cards */
.fusion-imageframe:hover,
.hover-type-zoomin:hover,
[class*="awb-card"]:hover {
  box-shadow: 0 0 40px var(--aii-glow), 0 0 80px rgba(139, 92, 246, 0.2) !important;
  transform: translateY(-2px);
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

/* Selection highlight */
::selection {
  background: var(--aii-primary);
  color: var(--aii-bg);
}

/* Scrollbar (Firefox) */
* { scrollbar-color: var(--aii-primary) var(--aii-bg-light); }
/* Scrollbar (Chromium) */
::-webkit-scrollbar { width: 10px; height: 10px; }
::-webkit-scrollbar-track { background: var(--aii-bg-light); }
::-webkit-scrollbar-thumb { background: var(--aii-primary); border-radius: 4px; }
</style>
"""

# Text replacement rules — visible brand text only (not in URLs/attributes).
# We match the literal strings inside text nodes, between > and < or in title/og:title/og:site_name meta values.
TEXT_REPLACEMENTS = [
    ("AIShotStudio", "AI Injection"),
    ("AI Shot Studio", "AI Injection"),
    ("AI SHOT STUDIO", "AI INJECTION"),
    ("AISHOTSTUDIO", "AI INJECTION"),
    # Tagline carryovers
    ("Limerick, Ireland", "AI Injection by PPR Holdings"),
    # Email — leave as-is so contact still routes; user can edit later
]


SKOOL_URL = "https://www.skool.com/ai-injection-4241"


def rebrand_html(path: Path) -> int:
    html = path.read_text(encoding="utf-8", errors="ignore")
    original = html

    # Strip any prior rebrand block (so re-running picks up CSS edits)
    html = re.sub(
        r'<!-- AI INJECTION REBRAND OVERRIDE -->.*?</style>',
        '',
        html, count=1, flags=re.S | re.I
    )
    # Inject fresh CSS override before </head>
    html = re.sub(r'</head>', AI_INJECTION_CSS + '\n</head>', html, count=1, flags=re.I)

    # === SKOOL REDIRECT — point all aischool community links to Rob's Skool ===
    # The original "AI School" Skool community link is aishotstudio.com/go/aischool (66+ occurrences across pages)
    for prefix in ("https://aishotstudio.com", "http://aishotstudio.com"):
        html = re.sub(
            re.escape(prefix + "/go/aischool") + r'/?(?=["\'\s>])',
            SKOOL_URL,
            html
        )

    # Text replacements — be careful only in visible text
    for old, new in TEXT_REPLACEMENTS:
        # 1. In <title> tags
        html = re.sub(r'(<title[^>]*>)([^<]*)' + re.escape(old) + r'([^<]*</title>)',
                      lambda m: m.group(1) + m.group(2) + new + m.group(3), html, flags=re.I)
        # 2. In meta content / og:tags
        html = re.sub(r'(<meta[^>]*content=")([^"]*)' + re.escape(old) + r'([^"]*"[^>]*>)',
                      lambda m: m.group(1) + m.group(2) + new + m.group(3), html, flags=re.I)
        # 3. In text nodes between > and <
        html = re.sub(r'(>[^<]*?)' + re.escape(old) + r'([^<]*?<)',
                      lambda m: m.group(1) + new + m.group(2), html)
        # 4. In alt= attributes (visible to screen readers)
        html = re.sub(r'(alt=")([^"]*)' + re.escape(old) + r'([^"]*")',
                      lambda m: m.group(1) + m.group(2) + new + m.group(3), html, flags=re.I)

    if html != original:
        path.write_text(html, encoding="utf-8")
        return 1
    return 0


def main():
    rebranded = 0
    for page_dir in sorted(PAGES.iterdir()):
        raw = page_dir / "raw.html"
        if not raw.exists():
            continue
        if rebrand_html(raw):
            rebranded += 1
            print(f"  rebranded: {page_dir.name}")
    print(f"\n=== {rebranded} pages rebranded ===")


if __name__ == "__main__":
    main()
