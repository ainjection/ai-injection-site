#!/usr/bin/env python3
"""Build a Prompt Generators page — 131 meta-prompt generators (no images, text-only).

Source: D:/airtable folder images with data/AI Video Engine - Prompt Generators
Output: pages/prompt-generators/raw.html

Distinct from the image-prompt galleries: these are meta-prompts you paste into ChatGPT/Claude
and they generate dozens of new prompts for you tailored to your subject.

Two filter rows:
  - Category: AI Video / Engineer / Top-Secret / JSON / Consistency / Cinematic / Template / All
  - Model: Sora / Veo 3 / Hailuo / Seedance / Runway / Kling / All Models
"""
import csv, os, re, html as ihtml, sys
from pathlib import Path

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path("C:/Users/clawb/Desktop/claudeclaw-main/site-clones/aishotstudio-full")
OUT_DIR = ROOT / "pages" / "prompt-generators"
TEMPLATE = ROOT / "pages" / "42-camera-movements" / "raw.html"
SRC_BASE = Path(r"D:/airtable folder images with data")

# Category filter row
CATEGORY_PILLS = [
    ("all", "All"),
    ("ai-video", "AI Video"),
    ("engineer", "Engineer"),
    ("top-secret", "Top-Secret"),
    ("consistency", "Consistency"),
    ("json", "JSON"),
    ("cinematic", "Cinematic"),
    ("dynamic", "Dynamic"),
    ("template", "Template"),
    ("seedance", "Seedance 2.0"),
    ("vip", "VIP 🔥"),
    ("mvp", "MVP ⭐"),
]

# Model filter row (operates as a parallel filter — separate from category)
MODEL_PILLS = [
    ("all-models", "All Models"),
    ("sora", "Sora"),
    ("veo", "Veo 3"),
    ("hailuo", "Hailuo / MiniMax"),
    ("seedance-model", "Seedance"),
    ("runway", "Runway"),
    ("kling", "Kling"),
    ("ltx", "LTX-2"),
    ("nb", "Nano Banana"),
]


def slugify_category(cat: str) -> str:
    s = re.sub(r"[\U0001F000-\U0001FFFF]", "", cat or "").strip().lower()
    if not s:
        return "ai-video"
    mapping = {
        "ai video": "ai-video",
        "engineer": "engineer",
        "top-secret": "top-secret",
        "consistent movie scene": "consistency",
        "json": "json",
        "seedance 2.0": "seedance",
        "dynamic": "dynamic",
        "template": "template",
        "cinematic": "cinematic",
        "image reference": "ai-video",
        "ltx-2": "ai-video",
        "full-length movie": "consistency",
        "idea x prompt enhancer": "engineer",
        "movie scene montage": "consistency",
        "cameras/lenses": "ai-video",
        "cut scenes": "consistency",
        "image to video": "ai-video",
        "multi-model": "ai-video",
        "runwayml": "ai-video",
        "viral": "ai-video",
    }
    return mapping.get(s, "ai-video")


def detect_models(text: str) -> list[str]:
    """Detect which model slugs apply to a given text blob (Type+Tags+Description+FullPrompt)."""
    t = text.lower()
    out = set()
    if "sora" in t: out.add("sora")
    if re.search(r"\bveo\b", t) or "veo 3" in t or "veo3" in t: out.add("veo")
    if "hailuo" in t or "minimax" in t: out.add("hailuo")
    if "seedance" in t: out.add("seedance-model")
    if "runway" in t or "gen-4" in t or "gen 4" in t: out.add("runway")
    if "kling" in t: out.add("kling")
    if "ltx" in t: out.add("ltx")
    if "nano banana" in t or "nano-banana" in t: out.add("nb")
    return sorted(out)


def find_source() -> Path:
    for d in os.listdir(SRC_BASE):
        if "AI Video Engine" in d and "Prompt Generators" in d:
            return SRC_BASE / d
    raise SystemExit("Source folder not found")


def clean_emoji_prefix(s: str) -> str:
    """Strip leading emoji + space from titles like '🧠 MiniMax Hailuo Generator'."""
    return re.sub(r"^[\U0001F000-\U0001FFFF\s\W]+", "", s or "").strip() or s


def build_card(num: int, row: dict) -> str:
    typ = (row.get("🚀Type") or "").strip()
    quick = (row.get("📝Quick Description") or "").strip()
    full = (row.get("🤖Full Prompt") or "").strip()
    cat = (row.get("🍿Category") or "").strip()
    tags = [t.strip() for t in (row.get("🔖Tags") or "").split(";") if t.strip()]
    is_mvp = (row.get("🏆MVP") or "").strip().lower() == "true"
    is_vip = bool((row.get("IF VIP") or "").strip())
    plen = (row.get("Prompt Length") or "").strip()

    # Title: prefer Quick Description (cleaned), fall back to Type
    title = quick or typ or f"Generator #{num}"
    # Strip leading "🧠 **" patterns and ** markdown
    title = re.sub(r"\*\*", "", title)
    title = re.sub(r"^[\s\W]*", lambda m: re.sub(r"[\U0001F000-\U0001FFFF]+", "", m.group(0)).strip() + " " if m.group(0).strip() else "", title)
    title = title.strip().strip("/").strip() or "Generator"
    title = title[:120]

    cat_slug = slugify_category(cat)
    # Combine all model slugs into one space-separated string
    model_slugs = detect_models(typ + " " + " ".join(tags) + " " + quick + " " + full[:500])
    badge_slugs = []
    if is_mvp: badge_slugs.append("mvp")
    if is_vip: badge_slugs.append("vip")
    category_attr = " ".join([cat_slug] + model_slugs + badge_slugs) or "ai-video"

    # Badges
    badges_html = []
    if is_vip:
        badges_html.append('<span style="display:inline-flex; align-items:center; gap:4px; padding:3px 9px; font-size:11px; font-weight:700; border-radius: 999px; background: linear-gradient(135deg, #FF6B35, #FFC93C); color: #1a1a35;">🔥 VIP</span>')
    if is_mvp:
        badges_html.append('<span style="display:inline-flex; align-items:center; gap:4px; padding:3px 9px; font-size:11px; font-weight:700; border-radius: 999px; background: linear-gradient(135deg, #FFD700, #FFA500); color: #1a1a35;">⭐ MVP</span>')

    cat_chip = (
        f'<span style="display:inline-block; padding:3px 9px; font-size:11px; border-radius: 999px; background: linear-gradient(135deg, rgba(0,212,255,0.2), rgba(139,92,246,0.2)); color: #fff; border: 1px solid rgba(139,92,246,0.4);">{ihtml.escape(cat)}</span>'
        if cat else ''
    )

    tag_chips = "".join(
        f'<span style="display:inline-block; padding:3px 9px; margin:2px 3px 0 0; font-size:11px; border-radius: 999px; background: rgba(0,212,255,0.12); color: #00D4FF; border: 1px solid rgba(0,212,255,0.3);">{ihtml.escape(t)}</span>'
        for t in tags[:4]
    )

    title_esc = ihtml.escape(title)
    full_esc = ihtml.escape(full)
    plen_disp = f'<span style="font-size:11px; color: rgba(255,255,255,0.4); margin-left:auto;">{plen} chars</span>' if plen else ''

    return f'''
        <div class="move-card extra-card generator-card" data-category="{category_attr}" style="background: rgba(255,255,255,0.04); border: 1px solid rgba(0,212,255,0.18); border-radius: 14px; padding: 22px; display: flex; flex-direction: column; gap: 12px;">
            <div class="card-content">
                <div style="display:flex; align-items:center; gap:10px; margin-bottom: 8px; flex-wrap: wrap;">
                  <span style="font-weight:900; font-size:18px; background: linear-gradient(135deg, #00D4FF, #8B5CF6); -webkit-background-clip: text; background-clip: text; -webkit-text-fill-color: transparent;">#{num}</span>
                  {cat_chip}
                  {''.join(badges_html)}
                  {plen_disp}
                </div>
                <h3 style="font-size: 18px; font-weight: 700; line-height: 1.3; margin: 0 0 8px 0; color: #fff;">{title_esc}</h3>
                <div style="margin-bottom: 12px;">{tag_chips}</div>
                <div class="prompt-container">
                    <div class="prompt-box" style="font-size: 13px; line-height: 1.55; max-height: 320px; overflow-y: auto; font-family: 'Consolas', 'Monaco', monospace; white-space: pre-wrap;">{full_esc}</div>
                    <button class="copy-icon-btn" onclick="navigator.clipboard.writeText(this.previousElementSibling.innerText); this.querySelector('.icon-copy').style.display='none'; this.querySelector('.icon-check').style.display='block'; setTimeout(()=>{{this.querySelector('.icon-copy').style.display='block'; this.querySelector('.icon-check').style.display='none';}}, 1500);">
                        <svg viewBox="0 0 24 24" class="icon-copy"><rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path></svg>
                        <svg viewBox="0 0 24 24" class="icon-check" style="display:none;"><polyline points="20 6 9 17 4 12"></polyline></svg>
                    </button>
                </div>
            </div>
        </div>'''


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    src = find_source()
    print(f"  source: {src}")

    with open(src / "data.csv", encoding="utf-8-sig", errors="ignore") as fp:
        rows = list(csv.DictReader(fp))

    # Sort: VIP first, then MVP, then by ID
    def sortkey(r):
        return (
            0 if r.get("IF VIP") else 1,
            0 if (r.get("🏆MVP") or "").lower() == "true" else 1,
            r.get("ID") or "999"
        )
    rows.sort(key=sortkey)

    cards = []
    for i, row in enumerate(rows, 1):
        full = (row.get("🤖Full Prompt") or "").strip()
        if not full or len(full) < 30:
            continue
        cards.append(build_card(i, row))

    print(f"  built {len(cards)} cards")

    # Read template
    tpl = TEMPLATE.read_text(encoding="utf-8")

    new_html = re.sub(
        r"<title[^>]*>[^<]*</title>",
        f"<title>Prompt Generators — {len(cards)} meta-prompts | AI Injection</title>",
        tpl, count=1, flags=re.I
    )
    new_html = re.sub(
        r"(<meta[^>]+name=\"description\"[^>]+content=\")[^\"]*(\")",
        rf"\g<1>{len(cards)} meta-prompt generators for AI video. Paste into ChatGPT/Claude — they generate dozens of optimized prompts tailored to your subject. Sora, Veo 3, Hailuo, Seedance, Runway, Kling.\g<2>",
        new_html, count=1, flags=re.I
    )
    new_html = re.sub(r"<h1([^>]*)>[^<]*</h1>", r'<h1\1>Prompt Generators</h1>', new_html, count=1)
    new_html = re.sub(
        r'<p style="text-align:center;[^"]*">[^<]*\(AI Injection edition\)</p>',
        f'<p style="text-align:center; color: rgba(255,255,255,0.5); font-size: 16px; margin-top: 8px;">{len(cards)} meta-prompt generators — paste into ChatGPT or Claude and they generate optimized prompts FOR you. Sora, Veo 3, Hailuo, Seedance, Runway, Kling.</p>',
        new_html, count=1
    )

    # Two filter rows
    cat_pills = "\n            ".join(
        f'<button class="filter-btn{" active" if slug == "all" else ""}" data-filter="{slug}">{label}</button>'
        for slug, label in CATEGORY_PILLS
    )
    model_pills = "\n            ".join(
        f'<button class="filter-btn model-pill{" active" if slug == "all-models" else ""}" data-filter="{slug}">{label}</button>'
        for slug, label in MODEL_PILLS
    )

    new_html = re.sub(
        r'<div id="filterContainer">[\s\S]*?</div>',
        f'<div id="filterContainer">\n            {cat_pills}\n        </div>\n        <div id="modelFilterContainer" style="display: flex; gap: 8px; flex-wrap: wrap; justify-content: center; align-items: center; width: 100%; margin-top: 14px;">\n            {model_pills}\n        </div>',
        new_html, count=1
    )

    # Wider cards — let the parent grid (.movement-grid) handle the 2-col layout (already does that on desktop)
    extra_css = '''
<style>
/* Prompt Generators — full-width within grid cells, 1-col on mobile */
.move-card.generator-card {
  width: 100% !important;
  max-width: 100% !important;
}
.move-card.generator-card .prompt-box {
  background: rgba(0,0,0,0.45) !important;
  width: 100% !important;
  box-sizing: border-box;
}
.move-card.generator-card .prompt-container {
  width: 100% !important;
}
.move-card.generator-card .card-content {
  width: 100% !important;
}
/* Mobile: single column */
@media (max-width: 768px) {
  body[data-page="prompt-generators"] .movement-grid {
    grid-template-columns: 1fr !important;
  }
}
</style>
'''
    new_html = re.sub(r"</head>", extra_css + "\n</head>", new_html, count=1, flags=re.I)
    # tag body so the CSS scopes correctly
    new_html = re.sub(r"<body([^>]*?)>", r'<body\1 data-page="prompt-generators">', new_html, count=1)

    # Replace move-cards block
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

    # Self-canonical
    new_html = re.sub(r'<link rel="canonical" href="[^"]*">', '<link rel="canonical" href="./raw.html">', new_html, count=1)
    new_html = re.sub(r'<meta property="og:url" content="[^"]*">', '<meta property="og:url" content="./raw.html">', new_html, count=1)

    # Replace the filter JS to support TWO independent filter rows: category + model.
    # Original filter logic: clicking a button activates only itself, sets one filter; cards show if their data-category includes it.
    # New logic: two rows. Each row has its own active. Cards show if data-category includes BOTH active filters.
    new_filter_js = '''
// === Two-row filter: category + model (AI Injection custom) ===
(function() {
    function applyDualFilter() {
        const catActive = document.querySelector('#filterContainer .filter-btn.active');
        const modelActive = document.querySelector('#modelFilterContainer .filter-btn.active');
        const catFilter = catActive ? catActive.getAttribute('data-filter') : 'all';
        const modelFilter = modelActive ? modelActive.getAttribute('data-filter') : 'all-models';
        document.querySelectorAll('.move-card').forEach(card => {
            const cats = card.getAttribute('data-category') || '';
            const matchCat = (catFilter === 'all') || cats.includes(catFilter);
            const matchModel = (modelFilter === 'all-models') || cats.includes(modelFilter);
            card.style.display = (matchCat && matchModel) ? 'flex' : 'none';
        });
    }
    function bindRow(rowSelector) {
        const btns = document.querySelectorAll(rowSelector + ' .filter-btn');
        btns.forEach(btn => btn.addEventListener('click', () => {
            btns.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            applyDualFilter();
        }));
    }
    document.addEventListener('DOMContentLoaded', () => {
        bindRow('#filterContainer');
        bindRow('#modelFilterContainer');
    });
})();
'''
    # Inject before </body>
    new_html = re.sub(r"</body>", f"<script>{new_filter_js}</script>\n</body>", new_html, count=1, flags=re.I)

    out_path = OUT_DIR / "raw.html"
    out_path.write_text(new_html, encoding="utf-8")
    print(f"  wrote {out_path}")
    print(f"  page size: {len(new_html):,} chars")


if __name__ == "__main__":
    main()
