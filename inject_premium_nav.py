#!/usr/bin/env python3
"""Inject a 'Premium' nav button + footer link on every page that points to
pages/premium/raw.html. Idempotent via marker comments.
"""
import re, sys
from pathlib import Path

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path("C:/Users/clawb/Desktop/claudeclaw-main/site-clones/aishotstudio-full")
PAGES = ROOT / "pages"
SKIP = {"premium", "get-the-pack"}

NAV_MARKER = "<!-- AI INJECTION PREMIUM NAV -->"
NAV_BUTTON = (
    f'{NAV_MARKER}'
    '<div style="text-align:right;margin-right:14px;">'
    '<a href="../premium/raw.html" '
    'style="display:inline-flex;align-items:center;gap:8px;'
    'padding:13px 28px;'
    'background:linear-gradient(135deg,#8B5CF6 0%,#00D4FF 100%);'
    'color:#0F0F23 !important;font-weight:900;font-size:17px;'
    'border-radius:28px;text-decoration:none;'
    'box-shadow:0 0 32px rgba(139,92,246,0.7),0 0 12px rgba(0,212,255,0.6);'
    'font-family:Inter,-apple-system,BlinkMacSystemFont,sans-serif;'
    'white-space:nowrap;text-transform:uppercase;letter-spacing:0.05em;'
    'border:2px solid rgba(255,255,255,0.15);'
    'animation:aii-prem-glow 2.4s ease-in-out infinite;">'
    '<span style="font-size:18px;">⚡</span> Premium</a>'
    '</div>'
    '<style>@keyframes aii-prem-glow{0%,100%{box-shadow:0 0 32px rgba(139,92,246,0.7),0 0 12px rgba(0,212,255,0.6);}50%{box-shadow:0 0 50px rgba(139,92,246,1),0 0 20px rgba(0,212,255,0.9);}}</style>'
)

# Inject the Premium button right BEFORE the YouTube button (which is the first
# button in the top-right nav row). Each page has it inside a wrapper that ends
# with `target="_blank" rel="noopener noreferrer" href="https://www.youtube.com/@AiInjection-i2p">`
# We anchor on the parent <div style="text-align:right;"><a class="fusion-button..."...href="https://www.youtube.com/@AiInjection-i2p">
# and insert our button just before it.
YT_NAV_RE = re.compile(
    r'(<div style="text-align:right;"><a class="fusion-button[^"]*"[^>]*href="https://www\.youtube\.com/@AiInjection-i2p")',
    re.IGNORECASE,
)
EXISTING_NAV_RE = re.compile(re.escape(NAV_MARKER) + r'.*?</div>\s*', re.IGNORECASE | re.DOTALL)


def inject(path: Path) -> int:
    html = path.read_text(encoding="utf-8", errors="ignore")
    html = EXISTING_NAV_RE.sub("", html)
    new_html, n = YT_NAV_RE.subn(lambda m: NAV_BUTTON + m.group(1), html, count=2)
    if n:
        path.write_text(new_html, encoding="utf-8")
    return n


def main():
    total = 0
    pages_touched = 0
    for page_dir in sorted(PAGES.iterdir()):
        raw = page_dir / "raw.html"
        if not raw.exists():
            continue
        if page_dir.name in SKIP:
            continue
        n = inject(raw)
        if n:
            pages_touched += 1
        total += n
    print(f"Injected Premium nav button on {pages_touched} pages ({total} occurrences total — most pages have 2 nav button rows for desktop + mobile).")


if __name__ == "__main__":
    main()
