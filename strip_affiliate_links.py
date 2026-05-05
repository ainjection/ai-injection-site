#!/usr/bin/env python3
"""Replace aishotstudio.com affiliate redirects with direct tool URLs.

Rob's call: no affiliate, just straight links to each tool's site. Run across
every page so it stays consistent if the same /go/ link is referenced elsewhere.
"""
import re, sys
from pathlib import Path

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path("C:/Users/clawb/Desktop/claudeclaw-main/site-clones/aishotstudio-full")
PAGES = ROOT / "pages"

# aishotstudio.com slug -> direct destination URL
DIRECT = {
    "go/11Labs":          "https://elevenlabs.io",
    "go/acestudio":       "https://acestudio.ai",
    "go/blip":            "https://blip.app",
    "go/fal":             "https://fal.ai",
    "go/flexclip":        "https://www.flexclip.com",
    "go/imagineart":      "https://www.imagine.art",
    "go/kie":             "https://kie.ai",
    "go/lama":            "https://lama.art",
    "go/loova":           "https://loova.app",
    "go/musiccreatorai":  "https://musiccreator.ai",
    "go/novi":            "https://novi.ai",
    "go/novita":          "https://novita.ai",
    "go/pippit":          "https://pippit.com",
    "go/replicate":       "https://replicate.com",
    "go/wavespeed":       "https://wavespeed.ai",
    "go/wisprflow":       "https://wisprflow.ai",
    "try/freepik":        "https://www.freepik.com",
    "try/fpspaces":       "https://www.freepik.com/spaces",
    "try/mindstudio":     "https://www.mindstudio.ai",
}


def build_replacements():
    out = []
    for slug, dest in DIRECT.items():
        for proto in ("https", "http"):
            src = f"{proto}://aishotstudio.com/{slug}"
            # match the URL when followed by a quote, space, or close-bracket — avoid partial matches
            pat = re.compile(re.escape(src) + r'(?=["\'\s>?#])', re.IGNORECASE)
            out.append((pat, dest))
    return out


def rewrite(path: Path, replacements) -> int:
    html = path.read_text(encoding="utf-8", errors="ignore")
    count = 0
    for pat, repl in replacements:
        html, n = pat.subn(repl, html)
        count += n
    if count:
        path.write_text(html, encoding="utf-8")
    return count


def main():
    repls = build_replacements()
    total = 0
    for page_dir in sorted(PAGES.iterdir()):
        if not page_dir.is_dir():
            continue
        raw = page_dir / "raw.html"
        if not raw.exists():
            continue
        n = rewrite(raw, repls)
        if n:
            print(f"  {page_dir.name:45} {n:3} links straightened")
        total += n
    print()
    print(f"=== {total} affiliate links replaced with direct URLs ===")


if __name__ == "__main__":
    main()
