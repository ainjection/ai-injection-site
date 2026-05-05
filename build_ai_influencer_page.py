#!/usr/bin/env python3
"""Build an AI Influencer Prompts page using the camera-movements page as visual template.

Source: D:/airtable folder images with data/Prompt Portal - AI Influencers_Podcast/
Output: pages/ai-influencer-prompts/raw.html + pages/ai-influencer-prompts/images/

553 records with reference images, 66 distinct tags. Top 10 tags become filter pills.
"""
import csv, os, re, html as ihtml, shutil, sys
from pathlib import Path
from collections import Counter

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path("C:/Users/clawb/Desktop/claudeclaw-main/site-clones/aishotstudio-full")
OUT_DIR = ROOT / "pages" / "ai-influencer-prompts"
OUT_IMG = OUT_DIR / "images"
TEMPLATE = ROOT / "pages" / "42-camera-movements" / "raw.html"

def _find_src_folder() -> Path:
    base = Path(r"D:/airtable folder images with data")
    for d in os.listdir(base):
        if "AI Influencers" in d and "Podcast" in d:
            return base / d
    raise SystemExit("could not locate AI Influencers source folder under D:")

SRC_FOLDER = _find_src_folder()
SRC_IMG = SRC_FOLDER / "images"
SRC_CSV = SRC_FOLDER / "data.csv"
print(f"  source: {SRC_FOLDER}")

# Top 10 tags become filter pills (slug -> display label)
FILTER_PILLS = [
    ("all", "All"),
    ("selfie", "Selfie"),
    ("podcast", "Podcast"),
    ("editorial", "Editorial"),
    ("beach", "Beach"),
    ("closeup", "Closeup"),
    ("fitness", "Fitness"),
    ("cyberpunk", "Cyberpunk"),
    ("casual", "Casual"),
    ("luxury", "Luxury"),
    ("fashion", "Fashion"),
    ("car", "Car"),
    ("paparazzi", "Paparazzi"),
    ("gamer", "Gamer"),
    ("fantasy", "Fantasy"),
]


def slugify_tag(tag: str) -> str:
    """Map a raw tag string to a filter-slug. Returns space-separated slugs for compound tags."""
    tag = tag.lower().strip()
    # remove emoji prefix
    tag = re.sub(r"[\U0001F000-\U0001FFFF]", "", tag).strip()
    if not tag:
        return ""
    mapping = {
        "selfie": "selfie",
        "podcast": "podcast",
        "talk show": "podcast",
        "editorial": "editorial",
        "beach": "beach",
        "closeup": "closeup",
        "fitness": "fitness",
        "cyberpunk": "cyberpunk",
        "casual": "casual",
        "luxury lifestyle": "luxury",
        "luxury": "luxury",
        "glam": "luxury",
        "fashion": "fashion",
        "car": "car",
        "paparazzi": "paparazzi",
        "gamer": "gamer",
        "streaming": "gamer",
        "fantasy": "fantasy",
        "pop star": "fashion",
        "music video": "fashion",
        "city": "casual",
        "street": "casual",
        "black and white": "editorial",
    }
    return mapping.get(tag, "")


def parse_tags(raw: str) -> tuple[str, list[str]]:
    """Return (data-category-string, list-of-display-tags) for a record's Tags field."""
    if not raw:
        return ("", [])
    parts = [p.strip() for p in raw.split(";") if p.strip()]
    slugs = set()
    display = []
    for p in parts:
        s = slugify_tag(p)
        if s:
            slugs.add(s)
        display.append(p)
    return (" ".join(sorted(slugs)), display)


def build_card_html(num: int, prompt: str, image_rel: str, display_tags: list[str], category_str: str, app: str) -> str:
    name_esc = ihtml.escape((display_tags[0] if display_tags else f"Prompt #{num}").title()[:60])
    desc_esc = ihtml.escape(prompt.strip())
    img_attr = ihtml.escape(image_rel)
    app_esc = ihtml.escape(app or "")
    tag_chips = "".join(
        f'<span style="display:inline-block; padding:3px 9px; margin:2px 3px 0 0; font-size:11px; border-radius: 999px; background: rgba(0,212,255,0.12); color: #00D4FF; border: 1px solid rgba(0,212,255,0.3);">{ihtml.escape(t)}</span>'
        for t in display_tags[:3]
    )

    return f'''
        <div class="move-card extra-card" data-category="{category_str or 'misc'}" style="background: rgba(255,255,255,0.04); border: 1px solid rgba(0,212,255,0.18); border-radius: 14px; padding: 18px; display: flex; flex-direction: column; gap: 14px;">
            <div class="video-wrapper" style="border-radius: 12px; overflow: hidden; aspect-ratio: 1/1; background: #000;">
                <img src="{img_attr}" alt="{name_esc}" loading="lazy" style="width: 100%; height: 100%; object-fit: cover;">
            </div>
            <div class="card-content">
                <div style="display:flex; align-items:center; gap:10px; margin-bottom: 6px; flex-wrap: wrap;">
                  <span style="font-weight:900; font-size:18px; background: linear-gradient(135deg, #00D4FF, #8B5CF6); -webkit-background-clip: text; background-clip: text; -webkit-text-fill-color: transparent;">#{num}</span>
                  {f'<span style="font-size:11px; color: rgba(255,255,255,0.5);">{app_esc}</span>' if app_esc else ''}
                </div>
                <div style="margin-bottom: 8px;">{tag_chips}</div>
                <div class="prompt-container">
                    <div class="prompt-box" style="font-size: 13px; line-height: 1.5; max-height: 180px; overflow-y: auto;">{desc_esc}</div>
                    <button class="copy-icon-btn" onclick="navigator.clipboard.writeText(this.previousElementSibling.innerText); this.querySelector('.icon-copy').style.display='none'; this.querySelector('.icon-check').style.display='block'; setTimeout(()=>{{this.querySelector('.icon-copy').style.display='block'; this.querySelector('.icon-check').style.display='none';}}, 1200);">
                        <svg viewBox="0 0 24 24" class="icon-copy"><rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path></svg>
                        <svg viewBox="0 0 24 24" class="icon-check" style="display:none;"><polyline points="20 6 9 17 4 12"></polyline></svg>
                    </button>
                </div>
            </div>
        </div>'''


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    OUT_IMG.mkdir(parents=True, exist_ok=True)

    # 1. Read source CSV
    with open(SRC_CSV, encoding="utf-8-sig", errors="ignore") as fp:
        rows = list(csv.DictReader(fp))

    # 2. Map record_id -> first image (Image_0) on disk
    all_imgs = os.listdir(SRC_IMG)
    by_record: dict[str, str] = {}
    for f in all_imgs:
        m = re.match(r"(rec[A-Za-z0-9]+)_Image_(\d+)_(.+)", f)
        if m:
            rid, idx = m.group(1), int(m.group(2))
            if rid not in by_record or idx < int(by_record[rid].split("_Image_")[1].split("_")[0]):
                by_record[rid] = f

    # 3. Build cards + copy images
    cards = []
    copied = 0
    skipped = 0
    num = 0
    for row in rows:
        rid = row.get("_record_id", "").strip()
        prompt = (row.get("Prompt") or "").strip()
        if not prompt or rid not in by_record:
            skipped += 1
            continue
        num += 1
        # Copy + rename image
        src_file = SRC_IMG / by_record[rid]
        if not src_file.exists():
            print(f"  WARN: src missing for {rid}: {src_file}")
            skipped += 1
            continue
        ext = src_file.suffix.lower() or ".png"
        dst_name = f"{rid}{ext}"
        dst = OUT_IMG / dst_name
        if not dst.exists():
            try:
                shutil.copy2(str(src_file), str(dst))
                copied += 1
            except Exception as e:
                print(f"  WARN: copy failed {src_file.name}: {e}")
                skipped += 1
                continue
        # Parse tags
        category_str, display_tags = parse_tags(row.get("Tags", ""))
        # Card
        cards.append(build_card_html(
            num=num,
            prompt=prompt,
            image_rel=f"images/{dst_name}",
            display_tags=display_tags,
            category_str=category_str,
            app=row.get("App", ""),
        ))
    print(f"  built {len(cards)} cards, copied {copied} new images, skipped {skipped} rows without prompt/image")

    # 4. Build filter pill HTML
    pills_html = "\n            ".join(
        f'<button class="filter-btn{" active" if slug == "all" else ""}" data-filter="{slug}">{label}</button>'
        for slug, label in FILTER_PILLS
    )

    # 5. Read template + extract head/body structure
    tpl = TEMPLATE.read_text(encoding="utf-8")

    # Update title
    new_html = re.sub(
        r"<title[^>]*>[^<]*</title>",
        "<title>AI Influencer Prompts — 553 prompts with reference images | AI Injection</title>",
        tpl, count=1, flags=re.I
    )
    # Update meta description / og:title / og:url where it appears
    new_html = re.sub(
        r"(<meta[^>]+name=\"description\"[^>]+content=\")[^\"]*(\")",
        r"\g<1>553 AI Influencer image prompts curated by AI Injection — copy, paste, generate. Filter by selfie, podcast, editorial, beach, fitness, cyberpunk, and more.\g<2>",
        new_html, count=1, flags=re.I
    )

    # Replace H1
    new_html = re.sub(
        r"<h1([^>]*)>[^<]*</h1>",
        r'<h1\1>AI Influencer Prompts</h1>',
        new_html, count=1
    )

    # Replace H1 subline (if any 42-with-video-previews leftover)
    new_html = re.sub(
        r'<p style="text-align:center;[^"]*">[^<]*\(AI Injection edition\)</p>',
        '<p style="text-align:center; color: rgba(255,255,255,0.5); font-size: 16px; margin-top: 8px;">553 prompts with reference images, click to copy. Curated by AI Injection.</p>',
        new_html, count=1
    )

    # Replace filter pills entirely
    new_html = re.sub(
        r'<div id="filterContainer">[\s\S]*?</div>',
        f'<div id="filterContainer">\n            {pills_html}\n        </div>',
        new_html, count=1
    )

    # Replace ALL move-cards (existing 42 + extra 30) with our new cards.
    # Strategy: find first <div class="move-card"... and remove from there until the closing of the parent grid.
    # The parent is the grid container that holds all cards. Find its bounds:
    # Look for the first move-card, then walk forward div-by-div until we reach the grid's closing.
    # Easier: replace from first <div class="move-card" through the LAST </div> before the search/filter section ends.

    first = re.search(r'<div class="move-card"[^>]*>', new_html)
    if not first:
        # try extra-card
        first = re.search(r'<div class="move-card extra-card"[^>]*>', new_html)
    if not first:
        print("  ERROR: no move-card anchor found in template")
        return
    start = first.start()

    # Walk forward counting div depth; collect ALL move-cards (consecutive). Stop when we hit a non-move-card sibling.
    # Simpler: find the LAST move-card's closing </div> and replace everything between the first and that.
    # Find all move-card opens
    matches = list(re.finditer(r'<div class="move-card[^"]*"[^>]*>', new_html))
    last_open = matches[-1].start()
    # Walk to find its closing
    depth = 0
    i = last_open
    end = i
    while i < len(new_html):
        m_open = re.match(r"<div\b[^>]*>", new_html[i:])
        m_close = re.match(r"</div>", new_html[i:])
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

    # Replace start..end with our new cards
    new_block = "\n".join(cards)
    new_html = new_html[:start] + new_block + new_html[end:]

    # 6. Fix relative asset paths — template lives at pages/42-camera-movements/, we live at pages/ai-influencer-prompts/
    # Both depths the same, so relative paths still resolve. But absolute /assets/ etc. work regardless.
    # However the template has links like `../home/raw.html` which still work at our depth.

    OUT_DIR_HTML = OUT_DIR / "raw.html"
    OUT_DIR_HTML.write_text(new_html, encoding="utf-8")
    print(f"  wrote {OUT_DIR_HTML}")
    print(f"  page size: {len(new_html):,} chars")


if __name__ == "__main__":
    main()
