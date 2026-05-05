#!/usr/bin/env python3
"""Inject AI Injection brand-matched Gumroad product cards on every page.

Each page gets ONE targeted product card (the most relevant of Rob's 11 Gumroad
listings) inserted ABOVE the footer / lead-magnet CTA. The cards open Gumroad's
overlay checkout via gumroad.js so visitors don't leave the site.

Idempotent — marker comment lets re-runs detect and replace prior injections.
"""
import re, sys
from pathlib import Path

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path("C:/Users/clawb/Desktop/claudeclaw-main/site-clones/aishotstudio-full")
PAGES = ROOT / "pages"
GUMROAD_HANDLE = "digitalexpress77"

MARKER = "<!-- AI INJECTION GUMROAD CARD -->"

# Product catalogue — each entry holds slug, title, eyebrow text, sub-line, cover image.
PRODUCTS = {
    "lforxm": {
        "title": "Cinematic Workflow — AI Video Studio",
        "eyebrow": "PRO TOOL · Desktop app",
        "sub": "Stop paying monthly for 10 different AI tools. 9 video models · 9 lip-sync models · 7 image tools — all in one app.",
        "image": "https://public-files.gumroad.com/1punv51g205v9m1z83l66erf04eg",
    },
    "lpwqiq": {
        "title": "Kling Cinematic Workflow",
        "eyebrow": "PRO TOOL · Desktop app",
        "sub": "Multi-shot AI filmmaking with locked character + voice. Built for creators who need more than one-off shots.",
        "image": "https://public-files.gumroad.com/92w3k4a76zw0j5opafr6kxbj3w67",
    },
    "yafrjf": {
        "title": "Nano Banana Prompt Builder (with source code)",
        "eyebrow": "PRO TOOL · Source code included",
        "sub": "Cinematic consistency without the monthly Higgsfield bill. Source code included so you own it forever.",
        "image": "https://public-files.gumroad.com/1tqdbcdvij9lg4lcd31e1b8weqdd",
    },
    "bymfa": {
        "title": "ALL-IN-ONE AI Influencer Auto-Post System",
        "eyebrow": "AUTOMATION · Stop posting manually",
        "sub": "Seedream Dashboard + auto-post pipeline. The system real AI influencers don't talk about.",
        "image": "https://public-files.gumroad.com/1punv51g205v9m1z83l66erf04eg",
    },
    "bwicqm": {
        "title": "Upload Once. Post Everywhere.",
        "eyebrow": "AUTOMATION · Windows desktop",
        "sub": "Upload one image or video → instantly publish to every connected platform. One click, one upload.",
        "image": "https://public-files.gumroad.com/6gkz2zw7nny0cjhziwoqzkrlhx6x",
    },
    "ioqrnn": {
        "title": "Video Agent Pro — Local AI Video Workstation",
        "eyebrow": "PRO TOOL · Runs on your laptop",
        "sub": "AI video editor that renders in seconds and writes its own code. Includes 3D Hero Library.",
        "image": "https://public-files.gumroad.com/isljhrrkcqpnad1caj7c217qfhos",
    },
    "pwmsoy": {
        "title": "The Ultimate AI Prompts Mega Library",
        "eyebrow": "MEGA BUNDLE · 5,280+ prompts",
        "sub": "Stop wasting hours crafting prompts. 5,280+ ready-to-use professional prompts across every category.",
        "image": "https://public-files.gumroad.com/3fhulsgsqhm3mvkj97uvndih3iu5",
    },
}

# Page slug → Gumroad slug
PAGE_TO_PRODUCT = {
    # cinematic / camera pages → Cinematic Workflow
    "42-camera-movements": "lforxm",
    "27-cinematic-looks-lighting": "lforxm",
    "26-camera-angles-shot-types": "lforxm",
    "higgsfield-camera-comparison": "lforxm",
    "higgsfield-focal-length": "lforxm",
    "higgsfield-aperture": "lforxm",
    "true-360-180-orbit": "lforxm",
    "still-camera-fix": "lforxm",
    "technical-portrait-poses": "lforxm",
    "character-actor-catwalk": "lforxm",
    "shot-design": "lforxm",
    # Kling / advanced AI video / viral short-form
    "viral-video-transitions": "lpwqiq",
    "phone-catch-seedance": "lpwqiq",
    "volleyball-freeze-seedance": "lpwqiq",
    "lacoste-crocodile-seedance": "lpwqiq",
    "morning-rush-seedance": "lpwqiq",
    "cockroaches-bed": "lpwqiq",
    "border-break-master": "lpwqiq",
    "gender-swap-prompts": "lpwqiq",
    # Nano Banana
    "nano-banana-json": "yafrjf",
    # AI Influencer
    "ai-influencer-prompts": "bymfa",
    # Music page → Upload Once Post Everywhere (cross-platform distribution)
    "music": "bwicqm",
    # Hub pages → Video Agent Pro
    "home": "ioqrnn",
    "ai-toolset": "ioqrnn",
    # Prompt library / generators / image gens / song genres / elevenlabs → Mega Library
    "prompt-library": "pwmsoy",
    "prompt-generators": "pwmsoy",
    "text-to-video-prompt-structure": "pwmsoy",
    "16-ai-image-generators": "pwmsoy",
    "elevenlabs-audio-tags": "pwmsoy",
    "46-song-genres": "pwmsoy",
}

# Skip pages that shouldn't have a Gumroad card (the lead-magnet landing page)
SKIP = {"get-the-pack"}


def build_card(slug: str) -> str:
    p = PRODUCTS[slug]
    url = f"https://{GUMROAD_HANDLE}.gumroad.com/l/{slug}"
    return f"""{MARKER}
<style id="aii-gumroad-card-style-{slug}">
  #aii-gumroad-{slug} {{
    margin: 40px auto;
    max-width: 1100px;
    background: linear-gradient(135deg, rgba(139,92,246,0.10) 0%, rgba(0,212,255,0.08) 100%), #0F0F23;
    border: 1px solid rgba(139,92,246,0.4);
    border-radius: 18px;
    overflow: hidden;
    display: flex;
    flex-wrap: wrap;
    box-shadow: 0 0 60px rgba(139,92,246,0.18);
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    color: #FFFFFF;
  }}
  #aii-gumroad-{slug} .aii-gr-cover {{
    flex: 0 0 280px;
    aspect-ratio: 1 / 1;
    background: #1a1a35 center/cover no-repeat;
    border-right: 1px solid rgba(255,255,255,0.06);
  }}
  #aii-gumroad-{slug} .aii-gr-body {{
    flex: 1 1 360px;
    padding: 32px 36px;
    display: flex;
    flex-direction: column;
    justify-content: center;
  }}
  #aii-gumroad-{slug} .aii-gr-eyebrow {{
    display: inline-block;
    font-size: 11px;
    letter-spacing: 0.22em;
    color: #8B5CF6;
    font-weight: 800;
    text-transform: uppercase;
    margin-bottom: 12px;
  }}
  #aii-gumroad-{slug} .aii-gr-title {{
    font-size: 26px;
    font-weight: 800;
    line-height: 1.18;
    margin: 0 0 12px;
    color: #fff;
    letter-spacing: -0.01em;
  }}
  #aii-gumroad-{slug} .aii-gr-sub {{
    font-size: 15px;
    color: #a8a8c0;
    margin: 0 0 24px;
    line-height: 1.5;
  }}
  #aii-gumroad-{slug} .aii-gr-cta {{
    align-self: flex-start;
    display: inline-flex;
    align-items: center;
    gap: 8px;
    padding: 14px 28px;
    background: linear-gradient(135deg, #8B5CF6 0%, #00D4FF 100%);
    color: #0F0F23 !important;
    font-weight: 800;
    font-size: 15px;
    border-radius: 28px;
    text-decoration: none;
    box-shadow: 0 0 30px rgba(139,92,246,0.5);
    transition: transform .15s ease, box-shadow .15s ease;
  }}
  #aii-gumroad-{slug} .aii-gr-cta:hover {{
    transform: translateY(-2px) scale(1.04);
    box-shadow: 0 0 50px rgba(139,92,246,0.8);
  }}
  @media (max-width: 720px) {{
    #aii-gumroad-{slug} {{ flex-direction: column; }}
    #aii-gumroad-{slug} .aii-gr-cover {{ flex: 0 0 auto; aspect-ratio: 16 / 9; width: 100%; }}
    #aii-gumroad-{slug} .aii-gr-title {{ font-size: 21px; }}
    #aii-gumroad-{slug} .aii-gr-body {{ padding: 24px 22px; }}
  }}
</style>
<aside id="aii-gumroad-{slug}" role="complementary">
  <div class="aii-gr-cover" style="background-image:url('{p['image']}');"></div>
  <div class="aii-gr-body">
    <div class="aii-gr-eyebrow">⚡ {p['eyebrow']}</div>
    <h3 class="aii-gr-title">{p['title']}</h3>
    <p class="aii-gr-sub">{p['sub']}</p>
    <a class="gumroad-button aii-gr-cta" href="{url}?wanted=true" data-gumroad-overlay-checkout="true">Get it on Gumroad →</a>
  </div>
</aside>
<script src="https://gumroad.com/js/gumroad.js" async></script>
"""

# Anchor: insert ABOVE the lead-magnet CTA marker (so order top→bottom is:
# content → Gumroad card → lead-magnet CTA → footer). Falls back to footer
# wrapper, then </body>.
LM_MARKER = "<!-- AI INJECTION LEAD MAGNET CTA -->"
FOOTER_RE = re.compile(r'<div\s+class="fusion-tb-footer fusion-footer"', re.IGNORECASE)
BODY_END_RE = re.compile(r'</body>', re.IGNORECASE)
EXISTING_RE = re.compile(re.escape(MARKER) + r'.*?</script>\s*', re.IGNORECASE | re.DOTALL)


def inject(path: Path, slug: str) -> str:
    html = path.read_text(encoding="utf-8", errors="ignore")
    html = EXISTING_RE.sub("", html)
    card = build_card(slug)
    if LM_MARKER in html:
        html = html.replace(LM_MARKER, card + "\n" + LM_MARKER, 1)
    else:
        m = FOOTER_RE.search(html) or BODY_END_RE.search(html)
        if not m:
            return "no anchor"
        html = html[:m.start()] + card + "\n" + html[m.start():]
    path.write_text(html, encoding="utf-8")
    return "injected"


def main():
    counts = {"injected": 0, "skipped": 0, "no mapping": 0, "no anchor": 0}
    for page_dir in sorted(PAGES.iterdir()):
        raw = page_dir / "raw.html"
        if not raw.exists():
            continue
        if page_dir.name in SKIP:
            counts["skipped"] += 1
            continue
        slug = PAGE_TO_PRODUCT.get(page_dir.name)
        if not slug:
            counts["no mapping"] += 1
            print(f"  ! {page_dir.name}: no product mapping")
            continue
        result = inject(raw, slug)
        if result == "injected":
            counts["injected"] += 1
        else:
            counts["no anchor"] += 1
            print(f"  ! {page_dir.name}: {result}")
    print(f"\nInjected: {counts['injected']}  Skipped: {counts['skipped']}  No mapping: {counts['no mapping']}  No anchor: {counts['no anchor']}")


if __name__ == "__main__":
    main()
