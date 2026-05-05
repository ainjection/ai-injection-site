#!/usr/bin/env python3
"""Rewrite internal aishotstudio.com links in every captured raw.html to point to local files.

Result: a fully navigable local site clone — clicking any link stays on localhost.
"""
import re
from pathlib import Path

ROOT = Path("C:/Users/clawb/Desktop/claudeclaw-main/site-clones/aishotstudio-full")
PAGES = ROOT / "pages"

# URL path -> local slug
URL_TO_SLUG = {
    "/": "home",
    "/shot-design": "shot-design",
    "/prompt-library": "prompt-library",
    "/ai-toolset": "ai-toolset",
    "/learn-ai": "learn-ai",
    "/42-camera-movements-ai-prompts": "42-camera-movements",
    "/27-cinematic-looks-lighting-for-ai-video-prompts": "27-cinematic-looks-lighting",
    "/26-camera-angles-shot-types": "26-camera-angles-shot-types",
    "/song-genres-and-subgenres-prompts": "46-song-genres",
    "/viral-video-transitions": "viral-video-transitions",
    "/text-to-video-prompt-structure": "text-to-video-prompt-structure",
    "/still-camera-how-to-fix-camera": "still-camera-fix",
    "/true-360-180-degree-camera-orbit": "true-360-180-orbit",
    "/higgsfield-camera-comparison": "higgsfield-camera-comparison",
    "/higgsfield-focal-length-examples": "higgsfield-focal-length",
    "/higgsfield-aperture-examples": "higgsfield-aperture",
    "/comparison-of-16-ai-image-generators": "16-ai-image-generators",
    "/elevenlabs-audio-tags-list": "elevenlabs-audio-tags",
    "/technical-portrait-poses-prompts": "technical-portrait-poses",
    "/gender-swap-image-and-video-prompts": "gender-swap-prompts",
    "/character-actor-catwalk": "character-actor-catwalk",
    "/border-break-video-master-prompt": "border-break-master",
    "/lacoste-crocodile-seedance-2-prompt": "lacoste-crocodile-seedance",
    "/morning-rush-seedance-2-prompt": "morning-rush-seedance",
    "/volleyball-freeze-frame-seedance-2-prompt": "volleyball-freeze-seedance",
    "/phone-catch-seedance-2-0-prompt": "phone-catch-seedance",
    "/cockroaches-bed": "cockroaches-bed",
}

# Music page is in a sibling folder
MUSIC_TARGET = "../../aishotstudio-music/raw/raw.html"


def make_replacements():
    """Build (regex_pattern, replacement) tuples in priority order (longest paths first)."""
    out = []
    # Music special case
    for prefix in ("https://aishotstudio.com", "http://aishotstudio.com"):
        for pth in ("/music/", "/music"):
            out.append((re.compile(re.escape(prefix + pth) + r'(?=["\'\s>])'), MUSIC_TARGET))
    # Sort URL paths by length desc so longer paths match first
    paths = sorted(URL_TO_SLUG.keys(), key=lambda p: -len(p))
    for path in paths:
        slug = URL_TO_SLUG[path]
        target = f"../{slug}/raw.html"
        for prefix in ("https://aishotstudio.com", "http://aishotstudio.com"):
            # With trailing slash
            full_with_slash = prefix + (path if path.endswith("/") else path + "/")
            out.append((re.compile(re.escape(full_with_slash) + r'(?=["\'\s>?#])'), target))
            # Without trailing slash
            full_no_slash = prefix + path.rstrip("/") if path != "/" else prefix
            out.append((re.compile(re.escape(full_no_slash) + r'(?=["\'\s>?#])'), target))
    return out


def rewrite_file(path: Path, replacements):
    html = path.read_text(encoding="utf-8", errors="ignore")
    orig_len = len(html)
    count = 0
    for pat, repl in replacements:
        new_html, n = pat.subn(repl, html)
        if n:
            html = new_html
            count += n
    if count:
        path.write_text(html, encoding="utf-8")
    return count


def main():
    repls = make_replacements()
    total = 0
    for page_dir in sorted(PAGES.iterdir()):
        raw = page_dir / "raw.html"
        if not raw.exists():
            continue
        n = rewrite_file(raw, repls)
        print(f"  {page_dir.name}: {n} links rewritten")
        total += n
    print(f"\n=== {total} total link rewrites ===")


if __name__ == "__main__":
    main()
