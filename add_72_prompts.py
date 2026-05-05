#!/usr/bin/env python3
"""Upgrade the cloned 42 Camera Movements page to Rob's 72 (extends, doesn't replace).

- Keeps the existing 42 cards (with video previews) as cards 1-42.
- Appends 30 new text-only cards for prompts 43-72 (the shot-type ones).
- Updates H1, page title, og tags, breadcrumbs from "42" -> "72".
- Updates the home page card "42 Camera Movements" -> "72 Camera Movements".
"""
import json, re, html as ihtml
from pathlib import Path

ROOT = Path("C:/Users/clawb/Desktop/claudeclaw-main/site-clones/aishotstudio-full")
PROMPTS = json.loads((ROOT / "rob-camera-72.json").read_text(encoding="utf-8"))
MEDIA = json.loads((ROOT / "rob-camera-72-media.json").read_text(encoding="utf-8"))["media"]

# Per-prompt category mapping for the new prompts (43-72).
# Existing filters in the page: all, dolly, zoom, drone, pan
# New filters we're adding: shots (Shot Types), angles (Angles), handheld (Handheld/Static)
CATEGORY_BY_NUM = {
    # Shot Types (new): close-ups, framing
    43: "shots", 44: "shots", 45: "shots", 46: "shots",
    53: "shots", 55: "shots", 57: "shots", 58: "shots", 62: "shots",
    # Angles (new): high/low/dutch/etc.
    47: "angles", 48: "angles", 49: "angles", 50: "angles", 51: "angles", 52: "angles",
    54: "angles", 56: "angles", 59: "angles", 60: "angles", 61: "angles",
    # Dolly/Track (existing)
    63: "dolly", 65: "dolly", 66: "dolly",
    # Drone/Crane (existing)
    64: "drone", 69: "drone", 70: "drone",
    # Handheld/Static (new)
    67: "handheld", 68: "handheld",
    # Pan/Tilt (existing)
    71: "pan", 72: "pan",
}

PAGE_PATH = ROOT / "pages/42-camera-movements/raw.html"
HOME_PATH = ROOT / "pages/home/raw.html"


def make_extra_card(num: int, name: str, description: str, category: str | None = None) -> str:
    if category is None:
        category = CATEGORY_BY_NUM.get(num, "shots")

    """Generate a card with media (video or image) matching the same Avada structure."""
    name_esc = ihtml.escape(name)
    desc_esc = ihtml.escape(description)

    # Media block — video or image from Rob's site
    media = MEDIA.get(str(num))
    if media and media.get("type") == "video":
        media_block = f'''<div class="video-wrapper" style="border-radius: 12px; overflow: hidden; aspect-ratio: 16/9; background: #000;">
                <video class="smart-video" loop muted playsinline autoplay src="{media['src']}" style="width: 100%; height: 100%; object-fit: cover;"></video>
            </div>'''
    elif media and media.get("type") == "img":
        media_block = f'''<div class="video-wrapper" style="border-radius: 12px; overflow: hidden; aspect-ratio: 16/9; background: #000;">
                <img src="{media['src']}" alt="{name_esc}" loading="lazy" style="width: 100%; height: 100%; object-fit: cover;">
            </div>'''
    else:
        media_block = ''

    return f'''
        <div class="move-card extra-card" data-category="{category}" style="background: rgba(255,255,255,0.04); border: 1px solid rgba(0,212,255,0.18); border-radius: 14px; padding: 22px; display: flex; flex-direction: column; gap: 16px;">
            {media_block}
            <div class="card-content">
                <div style="display:flex; align-items:center; gap:12px; margin-bottom: 6px;">
                  <span style="font-weight:900; font-size:22px; background: linear-gradient(135deg, #00D4FF, #8B5CF6); -webkit-background-clip: text; background-clip: text; -webkit-text-fill-color: transparent;">#{num}</span>
                </div>
                <h3 class="move-name fusion-responsive-typography-calculated" data-fontsize="24" data-lineheight="29px" style="--fontSize: 24; line-height: 1.2; margin-bottom: 12px;">{name_esc}</h3>
                <div class="prompt-container">
                    <div class="prompt-box">{desc_esc}</div>
                    <button class="copy-icon-btn" onclick="navigator.clipboard.writeText(this.previousElementSibling.innerText); this.querySelector('.icon-copy').style.display='none'; this.querySelector('.icon-check').style.display='block'; setTimeout(()=>{{this.querySelector('.icon-copy').style.display='block'; this.querySelector('.icon-check').style.display='none';}}, 1200);">
                        <svg viewBox="0 0 24 24" class="icon-copy"><rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path></svg>
                        <svg viewBox="0 0 24 24" class="icon-check" style="display:none;"><polyline points="20 6 9 17 4 12"></polyline></svg>
                    </button>
                </div>
            </div>
        </div>'''


def update_camera_page():
    html = PAGE_PATH.read_text(encoding="utf-8")

    # 0. IDEMPOTENT: remove any previously-added extra-card blocks first so re-runs don't duplicate.
    # Each extra-card is structured: <div class="move-card extra-card" ...>...</div> (one move-card depth)
    while True:
        # Find an extra-card open
        m = re.search(r'<div class="move-card extra-card"[^>]*>', html)
        if not m:
            break
        start = m.start()
        # Walk forward to find matching </div>
        depth = 0
        i = start
        while i < len(html):
            mo = re.match(r'<div\b[^>]*>', html[i:])
            mc = re.match(r'</div>', html[i:])
            if mo:
                depth += 1
                i += mo.end()
            elif mc:
                depth -= 1
                i += mc.end()
                if depth == 0:
                    break
            else:
                i += 1
        html = html[:start] + html[i:]

    # 0.5. Remove any prior subline "42 with video previews..." we injected
    html = re.sub(r'<p style="text-align:center;[^"]*">42 with video previews \+ 30 additional shot-type prompts \(AI Injection edition\)</p>', '', html)

    # 0.6. Inject three new filter pills (Shot Types, Angles, Handheld/Static) into #filterContainer
    # Idempotent: only adds buttons whose data-filter value isn't already present.
    new_pills = [
        ('shots', 'Shot Types'),
        ('angles', 'Angles'),
        ('handheld', 'Handheld / Static'),
    ]
    for f_val, f_label in new_pills:
        if f'data-filter="{f_val}"' in html:
            continue
        # Insert just before the closing </div> of #filterContainer
        new_btn = f'\n            <button class="filter-btn" data-filter="{f_val}">{f_label}</button>'
        html = re.sub(
            r'(<div id="filterContainer">[\s\S]*?)(\n\s*</div>)',
            lambda m, b=new_btn: m.group(1) + b + m.group(2),
            html, count=1
        )

    # 1. Update title tag, H1, meta, breadcrumbs — every "42 Camera Movements" -> "72 Camera Movements"
    # (deliberately do NOT rewrite the URL slug `42-camera-movements` — folder is still named that, and
    #  that string appears in nav links / canonical URLs / off-canvas menu hrefs site-wide)
    html = re.sub(r'42 Camera Movements', '72 Camera Movements', html)

    # 2. Find the LAST </div> that closes the .move-card grid container, and inject our 30 cards before it.
    # Strategy: find the position where the 42nd card ends, then insert. Use the last "move-card" closing pattern.
    # Better: find the parent grid container and inject before its closing tag.
    # Look for the LAST occurrence of `</div>\s*</div>\s*</div>` after the last move-card.
    # Simpler: find the last move-card, count its </div> closures, insert just after.

    # Find all positions of <div class="move-card"
    matches = list(re.finditer(r'<div class="move-card"[^>]*>', html))
    if not matches:
        print("  ERROR: no move-card found")
        return
    # Take the last move-card and find its closing — assume balanced 4 levels deep
    last_start = matches[-1].start()

    # Walk forward from last_start, count nested divs until we close the move-card itself
    depth = 0
    i = last_start
    end = i
    while i < len(html):
        m_open = re.match(r'<div\b[^>]*>', html[i:])
        m_close = re.match(r'</div>', html[i:])
        if m_open:
            depth += 1
            i += m_open.end()
        elif m_close:
            depth -= 1
            i += m_close.end()
            if depth == 0:
                end = i
                break
        else:
            i += 1

    extras = "\n".join(make_extra_card(p[0], p[1], p[2]) for p in PROMPTS if p[0] > 42)
    new_html = html[:end] + "\n" + extras + "\n" + html[end:]

    # 3. Add a notice in the H1 section that this is the extended 72-prompt edition (small subline)
    new_html = re.sub(
        r'(<h1[^>]*>)([^<]*72 Camera Movements[^<]*)(</h1>)',
        r'\1\2\3<p style="text-align:center; color: rgba(255,255,255,0.5); font-size: 16px; margin-top: 8px;">42 with video previews + 30 additional shot-type prompts (AI Injection edition)</p>',
        new_html, count=1
    )

    PAGE_PATH.write_text(new_html, encoding="utf-8")
    print(f"  added {len([p for p in PROMPTS if p[0] > 42])} extra cards (43-72)")
    print(f"  updated H1 + title + meta from 42 -> 72")


def update_home_card():
    html = HOME_PATH.read_text(encoding="utf-8")
    n = 0
    # Replace "42 Camera Movements" -> "72 Camera Movements" in visible text + alt + title attributes
    new_html, c1 = re.subn(r'42 Camera Movements', '72 Camera Movements', html)
    n += c1
    # Also replace any "42" near "Camera Movement" link text (image alt etc.)
    HOME_PATH.write_text(new_html, encoding="utf-8")
    print(f"  home page: {n} replacements")


def main():
    print("Updating Camera Movements page...")
    update_camera_page()
    print("\nUpdating home card...")
    update_home_card()
    print("\nDone. Run rebrand.py next to re-apply AI Injection styling.")


if __name__ == "__main__":
    main()
