#!/usr/bin/env python3
"""Fetch official logos for each tool on the AI Toolset page.

Strategy per tool (try in order, stop on first success):
1. Clearbit Logo API: https://logo.clearbit.com/<domain>?size=512  (free, no key)
2. DuckDuckGo icons: https://icons.duckduckgo.com/ip3/<domain>.ico
3. Google s2/favicons (always returns something): https://www.google.com/s2/favicons?domain=<domain>&sz=256

Brandfetch CDN is intentionally NOT used: without a client-id token it returns
the same placeholder PNG (sha256 78b7dbe1...) for every domain.

Saves to pages/ai-toolset/images/logos/<slug>.<ext>
"""
import os, sys, hashlib, urllib.request, urllib.error, re
from pathlib import Path

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path("C:/Users/clawb/Desktop/claudeclaw-main/site-clones/aishotstudio-full")
OUT = ROOT / "pages" / "ai-toolset" / "images" / "logos"
OUT.mkdir(parents=True, exist_ok=True)

# slug -> (display_name, domain, original_filename_pattern)
TOOLS = {
    "elevenlabs":      ("ElevenLabs",        "elevenlabs.io",   "ElevenLabs"),
    "acestudio":       ("Ace Studio",        "acestudio.ai",    "Ace-Studio-for-Filmmakers"),
    "blip":            ("Blip App",          "blip.app",        "Blip-App"),
    "fal":             ("Fal AI",            "fal.ai",          "Fal-AI"),
    "flexclip":        ("FlexClip",          "flexclip.com",    "FlexClip"),
    "freepik":         ("Freepik",           "freepik.com",     "Freepik"),
    "freepik-spaces":  ("Freepik Spaces",    "freepik.com",     "Freepik-Spaces"),
    "imagineart":      ("Imagine Art",       "imagine.art",     "ImagineArt"),
    "kie":             ("Kie AI",            "kie.ai",          "Kie-AI"),
    "lama-art":        ("Lama Art",          "lama.art",        "Lama-Art"),
    "loova":           ("Loova",             "loova.app",       "Loova"),
    "mindstudio":      ("MindStudio",        "mindstudio.ai",   "MindStudio"),
    "musiccreator":    ("Music Creator AI",  "musiccreator.ai", "Music-Creator-AI-generator"),
    "novi-ai":         ("Novi AI",           "novi.ai",         "Novi-AI"),
    "novita-ai":       ("Novita AI",         "novita.ai",       "Novita-AI"),
    "pippit":          ("Pippit",            "pippit.com",      "Pippit"),
    "replicate":       ("Replicate",         "replicate.com",   "Replicate"),
    "wavespeed":       ("WaveSpeed AI",      "wavespeed.ai",    "WaveSpeed-AI"),
    "wisprflow":       ("Wispr Flow",        "wisprflow.ai",    "Wispr-Flow"),
}


# Known placeholder/error responses we should reject as if the fetch failed.
# md5 of brandfetch's "no client id" placeholder PNG — we caught the script
# silently writing this 19 times in a row, so blocklist it forever.
PLACEHOLDER_HASHES = {
    "78b7dbe161cea7d15a3ee4e992ee8911",
}


def fetch(url: str, timeout: float = 8.0) -> bytes | None:
    try:
        req = urllib.request.Request(url, headers={
            "User-Agent": "Mozilla/5.0 (compatible; AI-Injection-bot/1.0)",
        })
        with urllib.request.urlopen(req, timeout=timeout) as r:
            data = r.read()
        if len(data) < 200:
            return None
        if hashlib.md5(data).hexdigest() in PLACEHOLDER_HASHES:
            return None
        return data
    except Exception:
        return None


def fetch_logo(slug: str, name: str, domain: str) -> tuple[bytes, str] | None:
    sources = [
        ("clearbit",   f"https://logo.clearbit.com/{domain}?size=512"),
        ("duckduckgo", f"https://icons.duckduckgo.com/ip3/{domain}.ico"),
        ("google",     f"https://www.google.com/s2/favicons?domain={domain}&sz=256"),
    ]
    for src, url in sources:
        data = fetch(url)
        if data:
            return data, src
    return None


def main():
    print("Fetching tool logos...")
    print()
    results = {}
    for slug, (name, domain, _) in TOOLS.items():
        print(f"  {name:25} ({domain})", end=" ... ", flush=True)
        result = fetch_logo(slug, name, domain)
        if result:
            data, src = result
            ext = ".png"
            if data[:4] == b"\x89PNG":
                ext = ".png"
            elif data[:3] == b"GIF":
                ext = ".gif"
            elif data[:2] == b"\xff\xd8":
                ext = ".jpg"
            elif data[:5] == b"<?xml" or data[:4] == b"<svg":
                ext = ".svg"
            elif data[:4] == b"\x00\x00\x01\x00":
                ext = ".ico"
            out_path = OUT / f"{slug}{ext}"
            with open(out_path, "wb") as f:
                f.write(data)
            print(f"OK ({src}, {len(data):,} bytes, {ext})")
            results[slug] = out_path.name
        else:
            print("FAILED — no source returned a logo")
            results[slug] = None
    print()
    print(f"Got logos for {sum(1 for v in results.values() if v)}/{len(TOOLS)} tools")
    return results


if __name__ == "__main__":
    main()
