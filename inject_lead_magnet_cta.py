#!/usr/bin/env python3
"""Inject a 'Get the Master Pack' CTA card into every page just before the
footer, driving traffic to pages/get-the-pack/raw.html. Idempotent: marker
comment lets re-runs detect and replace prior injections.
"""
import re, sys
from pathlib import Path

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path("C:/Users/clawb/Desktop/claudeclaw-main/site-clones/aishotstudio-full")
PAGES = ROOT / "pages"

MARKER = "<!-- AI INJECTION LEAD MAGNET CTA -->"

CTA_HTML = f"""{MARKER}
<style id="aii-leadmagnet-cta-style">
  #aii-leadmagnet {{
    margin: 60px auto 40px;
    max-width: 1100px;
    padding: 36px 32px;
    background: linear-gradient(135deg, rgba(0,212,255,0.10) 0%, rgba(139,92,246,0.10) 100%), #0F0F23;
    border: 1px solid rgba(0,212,255,0.4);
    border-radius: 18px;
    box-shadow: 0 0 60px rgba(0,212,255,0.15);
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    justify-content: space-between;
    gap: 24px;
    color: #FFFFFF;
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
  }}
  #aii-leadmagnet .aii-lm-text {{ flex: 1 1 460px; }}
  #aii-leadmagnet .aii-lm-eyebrow {{
    display: inline-block;
    font-size: 11px;
    letter-spacing: 0.25em;
    color: #00D4FF;
    font-weight: 800;
    text-transform: uppercase;
    margin-bottom: 10px;
  }}
  #aii-leadmagnet .aii-lm-headline {{
    font-size: 26px;
    font-weight: 800;
    line-height: 1.15;
    margin: 0 0 8px;
    color: #fff;
    letter-spacing: -0.01em;
  }}
  #aii-leadmagnet .aii-lm-sub {{
    font-size: 15px;
    color: #a8a8c0;
    margin: 0;
    line-height: 1.5;
  }}
  #aii-leadmagnet .aii-lm-btn {{
    display: inline-flex;
    align-items: center;
    gap: 8px;
    padding: 14px 28px;
    background: linear-gradient(135deg, #00D4FF 0%, #8B5CF6 100%);
    color: #0F0F23 !important;
    font-weight: 800;
    font-size: 15px;
    border-radius: 28px;
    text-decoration: none;
    box-shadow: 0 0 30px rgba(0,212,255,0.5);
    transition: transform .15s ease, box-shadow .15s ease;
    flex: 0 0 auto;
    white-space: nowrap;
  }}
  #aii-leadmagnet .aii-lm-btn:hover {{
    transform: translateY(-2px) scale(1.04);
    box-shadow: 0 0 50px rgba(0,212,255,0.8);
  }}
  @media (max-width: 600px) {{
    #aii-leadmagnet {{ padding: 24px 20px; }}
    #aii-leadmagnet .aii-lm-headline {{ font-size: 21px; }}
    #aii-leadmagnet .aii-lm-btn {{ padding: 12px 22px; font-size: 14px; }}
  }}
</style>
<div id="aii-leadmagnet" role="complementary">
  <div class="aii-lm-text">
    <div class="aii-lm-eyebrow">📥 Free download</div>
    <h3 class="aii-lm-headline">Want all 200+ AI prompts in ONE PDF?</h3>
    <p class="aii-lm-sub">Camera moves · lighting · shot types · song genres · transitions · prompt structure. Yours forever. No credit card.</p>
  </div>
  <a class="aii-lm-btn" href="../get-the-pack/raw.html">Get the Master Pack →</a>
</div>
"""

# The cloned Avada theme wraps its footer as
#   <div class="fusion-tb-footer fusion-footer">…</div>
# Inject ABOVE that. Standard <footer> tag is the next fallback, then </body>.
FOOTER_RE = re.compile(
    r'(<div\s+class="fusion-tb-footer fusion-footer"|<footer\b)',
    re.IGNORECASE,
)
BODY_END_RE = re.compile(r'</body>', re.IGNORECASE)
EXISTING_RE = re.compile(re.escape(MARKER) + r'.*?</div>\s*', re.IGNORECASE | re.DOTALL)

# Pages to skip — the lead magnet landing page itself, and any others that
# already promote the pack
SKIP = {"get-the-pack"}


def inject(path: Path) -> str:
    html = path.read_text(encoding="utf-8", errors="ignore")
    # Strip prior injection so re-runs are clean
    html = EXISTING_RE.sub("", html)
    m = FOOTER_RE.search(html)
    if m:
        new_html = html[:m.start()] + CTA_HTML + "\n" + html[m.start():]
    else:
        m = BODY_END_RE.search(html)
        if not m:
            return "no <footer> or </body>"
        new_html = html[:m.start()] + CTA_HTML + "\n" + html[m.start():]
    path.write_text(new_html, encoding="utf-8")
    return "injected"


def main():
    counts = {"injected": 0, "skipped": 0, "no anchor": 0}
    for page_dir in sorted(PAGES.iterdir()):
        raw = page_dir / "raw.html"
        if not raw.exists():
            continue
        if page_dir.name in SKIP:
            counts["skipped"] += 1
            continue
        result = inject(raw)
        if result == "injected":
            counts["injected"] += 1
        else:
            counts["no anchor"] += 1
            print(f"  ! {page_dir.name}: {result}")
    print(f"\nInjected: {counts['injected']}  Skipped: {counts['skipped']}  No anchor: {counts['no anchor']}")


if __name__ == "__main__":
    main()
