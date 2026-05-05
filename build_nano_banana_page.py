#!/usr/bin/env python3
"""Build a Nano Banana JSON Prompts page — only records that have images.

Sources (3 subfolders under D:/airtable folder images with data):
  - Nano Banana _ JSON - Images
  - Nano Banana _ JSON - AI Influencers
  - Nano Banana _ JSON - JSON

Output: pages/nano-banana-json/raw.html + pages/nano-banana-json/images/

321 records with reference images. Filter pills built from the Style field.
"""
import csv, os, re, html as ihtml, shutil, sys
from pathlib import Path

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path("C:/Users/clawb/Desktop/claudeclaw-main/site-clones/aishotstudio-full")
OUT_DIR = ROOT / "pages" / "nano-banana-json"
OUT_IMG = OUT_DIR / "images"
TEMPLATE = ROOT / "pages" / "42-camera-movements" / "raw.html"

SRC_BASE = Path(r"D:/airtable folder images with data")

FILTER_PILLS = [
    ("all", "All"),
    ("ai-influencer", "AI Influencer"),
    ("paparazzi", "Paparazzi"),
    ("cinematic", "Cinematic"),
    ("editorial", "Editorial"),
    ("unique", "Unique"),
    ("ad-product", "Ad / Product"),
    ("3d-render", "3D Render"),
    ("cyberpunk", "Cyberpunk"),
    ("thumbnail", "Thumbnail"),
    ("brand", "Brand"),
    ("ui-design", "UI / Design"),
    ("tech", "Tech"),
    ("game", "Video Game"),
    ("misc", "Other"),
]


def slugify_style(style: str) -> str:
    s = re.sub(r"[\U0001F000-\U0001FFFF]", "", style or "").strip().lower()
    if not s:
        return "misc"
    mapping = {
        "ai influencer": "ai-influencer",
        "candid paparazzi": "paparazzi",
        "cinematic": "cinematic",
        "editorial": "editorial",
        "unique": "unique",
        "ad/product": "ad-product",
        "3d render": "3d-render",
        "futuristic/cyberpunk": "cyberpunk",
        "thumbnail": "thumbnail",
        "brand": "brand",
        "ui/design": "ui-design",
        "tech": "tech",
        "video game": "game",
        "selfie": "ai-influencer",
        "social media": "ai-influencer",
        "professional photoshoot": "editorial",
        "image grid": "misc",
        "greenscreen": "misc",
        "movie poster": "thumbnail",
        "infographic": "ui-design",
        "character sheet": "ai-influencer",
        "sketch": "misc",
        "upscale": "misc",
        "scenery": "misc",
        "isometric": "3d-render",
        "cctv": "misc",
        "poster": "thumbnail",
        "portrait": "ai-influencer",
        "json": "misc",
    }
    return mapping.get(s, "misc")


def find_subfolders() -> list[Path]:
    out = []
    for d in os.listdir(SRC_BASE):
        if "Nano Banana" in d and "Prompt Generators" not in d:
            out.append(SRC_BASE / d)
    return out


def build_card_html(num: int, prompt: str, image_rel: str, style: str, tags: list[str], category_slug: str) -> str:
    name_esc = ihtml.escape(style.title()[:60] if style else f"Prompt #{num}")
    desc_esc = ihtml.escape(prompt.strip())
    img_attr = ihtml.escape(image_rel)
    tag_chips = "".join(
        f'<span style="display:inline-block; padding:3px 9px; margin:2px 3px 0 0; font-size:11px; border-radius: 999px; background: rgba(0,212,255,0.12); color: #00D4FF; border: 1px solid rgba(0,212,255,0.3);">{ihtml.escape(t)}</span>'
        for t in tags[:3]
    )
    style_chip = (
        f'<span style="display:inline-block; padding:3px 9px; font-size:11px; border-radius: 999px; background: linear-gradient(135deg, rgba(0,212,255,0.2), rgba(139,92,246,0.2)); color: #fff; border: 1px solid rgba(139,92,246,0.4);">{ihtml.escape(style)}</span>'
        if style else ''
    )

    return f'''
        <div class="move-card extra-card" data-category="{category_slug}" style="background: rgba(255,255,255,0.04); border: 1px solid rgba(0,212,255,0.18); border-radius: 14px; padding: 18px; display: flex; flex-direction: column; gap: 14px;">
            <div class="video-wrapper" style="border-radius: 12px; overflow: hidden; aspect-ratio: 1/1; background: #000;">
                <img src="{img_attr}" alt="{name_esc}" loading="lazy" style="width: 100%; height: 100%; object-fit: cover;">
            </div>
            <div class="card-content">
                <div style="display:flex; align-items:center; gap:10px; margin-bottom: 6px; flex-wrap: wrap;">
                  <span style="font-weight:900; font-size:18px; background: linear-gradient(135deg, #00D4FF, #8B5CF6); -webkit-background-clip: text; background-clip: text; -webkit-text-fill-color: transparent;">#{num}</span>
                  {style_chip}
                </div>
                <div style="margin-bottom: 8px;">{tag_chips}</div>
                <div class="prompt-container">
                    <div class="prompt-box" style="font-size: 12px; line-height: 1.5; max-height: 220px; overflow-y: auto; font-family: 'Consolas', 'Monaco', monospace; white-space: pre-wrap;">{desc_esc}</div>
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

    cards = []
    copied = 0
    skipped = 0
    num = 0
    seen_record_ids = set()  # dedupe across subfolders

    for folder in find_subfolders():
        print(f"  scanning: {folder.name}")
        img_dir = folder / "images"
        if not img_dir.exists():
            continue
        # Map record_id -> first image
        by_record: dict[str, str] = {}
        for f in os.listdir(img_dir):
            m = re.match(r"(rec[A-Za-z0-9]+)_Image_(\d+)_(.+)", f)
            if m:
                rid, idx = m.group(1), int(m.group(2))
                if rid not in by_record:
                    by_record[rid] = f
                else:
                    # keep lowest index
                    cur_idx = int(by_record[rid].split("_Image_")[1].split("_")[0])
                    if idx < cur_idx:
                        by_record[rid] = f

        with open(folder / "data.csv", encoding="utf-8-sig", errors="ignore") as fp:
            rows = list(csv.DictReader(fp))

        for row in rows:
            rid = (row.get("_record_id") or "").strip()
            prompt = (row.get("Prompt") or "").strip()
            if not prompt or rid not in by_record:
                skipped += 1
                continue
            if rid in seen_record_ids:
                continue  # dedupe (record may appear in multiple subfolder exports)
            seen_record_ids.add(rid)

            src_file = img_dir / by_record[rid]
            if not src_file.exists():
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
                    print(f"  WARN copy {src_file.name}: {e}")
                    skipped += 1
                    continue

            num += 1
            style = (row.get("Style") or "").strip()
            tags_raw = (row.get("Tags") or "").strip()
            display_tags = [t.strip() for t in tags_raw.split(";") if t.strip() and t.strip() != "JSON"]
            slug = slugify_style(style)

            cards.append(build_card_html(
                num=num,
                prompt=prompt,
                image_rel=f"images/{dst_name}",
                style=style,
                tags=display_tags,
                category_slug=slug,
            ))

    print(f"  built {len(cards)} cards, copied {copied} new images, skipped {skipped}")

    # Build filter pills
    pills_html = "\n            ".join(
        f'<button class="filter-btn{" active" if slug == "all" else ""}" data-filter="{slug}">{label}</button>'
        for slug, label in FILTER_PILLS
    )

    # Read template
    tpl = TEMPLATE.read_text(encoding="utf-8")

    new_html = re.sub(
        r"<title[^>]*>[^<]*</title>",
        f"<title>Nano Banana JSON Prompts — {len(cards)} prompts with reference images | AI Injection</title>",
        tpl, count=1, flags=re.I
    )
    new_html = re.sub(
        r"(<meta[^>]+name=\"description\"[^>]+content=\")[^\"]*(\")",
        rf"\g<1>{len(cards)} structured JSON prompts for Nano Banana / Nano Banana Pro — copy, paste, generate. Filter by AI Influencer, Paparazzi, Cinematic, Editorial, and more.\g<2>",
        new_html, count=1, flags=re.I
    )
    new_html = re.sub(
        r"<h1([^>]*)>[^<]*</h1>",
        r'<h1\1>Nano Banana JSON Prompts</h1>',
        new_html, count=1
    )
    new_html = re.sub(
        r'<p style="text-align:center;[^"]*">[^<]*\(AI Injection edition\)</p>',
        f'<p style="text-align:center; color: rgba(255,255,255,0.5); font-size: 16px; margin-top: 8px;">{len(cards)} structured JSON prompts with reference images, click to copy. Curated by AI Injection.</p>',
        new_html, count=1
    )
    new_html = re.sub(
        r'<div id="filterContainer">[\s\S]*?</div>',
        f'<div id="filterContainer">\n            {pills_html}\n        </div>',
        new_html, count=1
    )

    # Replace all .move-card[s] with our cards
    matches = list(re.finditer(r'<div class="move-card[^"]*"[^>]*>', new_html))
    if not matches:
        print("  ERROR: no move-card anchor")
        return
    start = matches[0].start()
    last_open = matches[-1].start()
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

    new_block = "\n".join(cards)
    new_html = new_html[:start] + new_block + new_html[end:]

    # Self-reference canonical / og:url
    new_html = re.sub(r'<link rel="canonical" href="[^"]*">', '<link rel="canonical" href="./raw.html">', new_html, count=1)
    new_html = re.sub(r'<meta property="og:url" content="[^"]*">', '<meta property="og:url" content="./raw.html">', new_html, count=1)

    out_path = OUT_DIR / "raw.html"
    out_path.write_text(new_html, encoding="utf-8")
    print(f"  wrote {out_path}")
    print(f"  page size: {len(new_html):,} chars")


if __name__ == "__main__":
    main()
