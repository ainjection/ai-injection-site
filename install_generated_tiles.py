#!/usr/bin/env python3
"""Download AI-generated showcase tiles and overwrite the existing .webp files
in pages/ai-toolset/images/ so the page picks them up without HTML changes.

Also regenerates the responsive srcset thumbnails (200x113, 400x225, etc).
"""
import sys, urllib.request
from pathlib import Path
from io import BytesIO
from PIL import Image

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path("C:/Users/clawb/Desktop/claudeclaw-main/site-clones/aishotstudio-full")
IMAGES = ROOT / "pages" / "ai-toolset" / "images"
GEN = IMAGES / "generated"
GEN.mkdir(parents=True, exist_ok=True)

# slug -> (url, list of output basenames matching the existing webp filenames)
TILES = {
    "elevenlabs": (
        "https://d8j0ntlcm91z4.cloudfront.net/user_2x9Q7xsTJdAXnAoIDAoWEOIPy6b/hf_20260504_072901_ff6e75cf-096b-42a2-a986-5f9ea4cb59ef.png",
        ["ElevenLabs"],
        [(200,113),(400,226),(600,339),(800,452)],
    ),
    "pippit": (
        "https://d8j0ntlcm91z4.cloudfront.net/user_2x9Q7xsTJdAXnAoIDAoWEOIPy6b/hf_20260504_072906_7ba9f408-0bd5-4602-b106-d2789d1f10cd.png",
        ["Pippit"],
        [(200,113)],
    ),
    "replicate": (
        "https://d8j0ntlcm91z4.cloudfront.net/user_2x9Q7xsTJdAXnAoIDAoWEOIPy6b/hf_20260504_072911_35416640-552a-4dbf-89b3-448b99cc7405.png",
        ["Replicate"],
        [(200,113)],
    ),
    "acestudio": (
        "https://d8j0ntlcm91z4.cloudfront.net/user_2x9Q7xsTJdAXnAoIDAoWEOIPy6b/hf_20260504_073345_306ec79d-b6cd-4d9c-92c7-fc353b923f34.png",
        ["Ace-Studio-for-Filmmakers"],
        [(200,113)],
    ),
    "blip": (
        "https://d8j0ntlcm91z4.cloudfront.net/user_2x9Q7xsTJdAXnAoIDAoWEOIPy6b/hf_20260504_073350_91cb09c5-fa22-49b6-8e45-e875a7b79e4d.png",
        ["Blip-App"],
        [(200,112),(400,225)],
    ),
    "fal": (
        "https://d8j0ntlcm91z4.cloudfront.net/user_2x9Q7xsTJdAXnAoIDAoWEOIPy6b/hf_20260504_073354_cbc5e568-0cc5-449e-b67f-a9f3156a95f0.png",
        ["Fal-AI"],
        [(200,113)],
    ),
    "flexclip": (
        "https://d8j0ntlcm91z4.cloudfront.net/user_2x9Q7xsTJdAXnAoIDAoWEOIPy6b/hf_20260504_073359_cd15222e-2e90-411b-bd79-be50cfc8e59a.png",
        ["FlexClip"],
        [(200,113)],
    ),
    "freepik": (
        "https://d8j0ntlcm91z4.cloudfront.net/user_2x9Q7xsTJdAXnAoIDAoWEOIPy6b/hf_20260504_073404_6cca5c8c-966a-43f3-a782-92181baaf262.png",
        ["Freepik"],
        [(200,113)],
    ),
    "freepik-spaces": (
        "https://d8j0ntlcm91z4.cloudfront.net/user_2x9Q7xsTJdAXnAoIDAoWEOIPy6b/hf_20260504_073410_bb1c7155-61aa-417f-a8ee-49a1f4dc4b91.png",
        ["Freepik-Spaces"],
        [(200,112),(400,225)],
    ),
    "imagineart": (
        "https://d8j0ntlcm91z4.cloudfront.net/user_2x9Q7xsTJdAXnAoIDAoWEOIPy6b/hf_20260504_073414_563d60d1-8cdf-4715-a4e8-71dca6b7778c.png",
        ["ImagineArt"],
        [(200,113)],
    ),
    "kie": (
        "https://d8j0ntlcm91z4.cloudfront.net/user_2x9Q7xsTJdAXnAoIDAoWEOIPy6b/hf_20260504_073419_5ad051e6-bf1c-497b-9afb-66fedb782eb7.png",
        ["Kie-AI"],
        [(200,113)],
    ),
    "lama-art": (
        "https://d8j0ntlcm91z4.cloudfront.net/user_2x9Q7xsTJdAXnAoIDAoWEOIPy6b/hf_20260504_073423_804479f3-f921-4f72-8297-513c1c7f1df0.png",
        ["Lama-Art"],
        [(200,112),(400,225)],
    ),
    "loova": (
        "https://d8j0ntlcm91z4.cloudfront.net/user_2x9Q7xsTJdAXnAoIDAoWEOIPy6b/hf_20260504_073428_c25fdfb4-c1b2-40e2-bbd7-6a17ac6a3ac1.png",
        ["Loova"],
        [(200,113)],
    ),
    "mindstudio": (
        "https://d8j0ntlcm91z4.cloudfront.net/user_2x9Q7xsTJdAXnAoIDAoWEOIPy6b/hf_20260504_073433_272f0091-d8fa-4352-9463-bdaa4b373471.png",
        ["MindStudio"],
        [(200,113)],
    ),
    "musiccreator": (
        "https://d8j0ntlcm91z4.cloudfront.net/user_2x9Q7xsTJdAXnAoIDAoWEOIPy6b/hf_20260504_073437_7e7ad694-cb8e-4db1-aaf2-9d488408d9fe.png",
        ["Music-Creator-AI-generator"],
        [(200,113)],
    ),
    "novi-ai": (
        "https://d8j0ntlcm91z4.cloudfront.net/user_2x9Q7xsTJdAXnAoIDAoWEOIPy6b/hf_20260504_073441_5f19c615-d771-4a95-950d-f89cb7c8d5f0.png",
        ["Novi-AI"],
        [(200,112),(400,225)],
    ),
    "novita-ai": (
        "https://d8j0ntlcm91z4.cloudfront.net/user_2x9Q7xsTJdAXnAoIDAoWEOIPy6b/hf_20260504_073446_1eb587eb-970f-4938-adf3-aa587884714f.png",
        ["Novita-AI"],
        [(200,113)],
    ),
    "wavespeed": (
        "https://d8j0ntlcm91z4.cloudfront.net/user_2x9Q7xsTJdAXnAoIDAoWEOIPy6b/hf_20260504_073450_9e6120c0-f50e-4db8-b1ef-5f92734dcad9.png",
        ["WaveSpeed-AI"],
        [(200,113)],
    ),
    "wisprflow": (
        "https://d8j0ntlcm91z4.cloudfront.net/user_2x9Q7xsTJdAXnAoIDAoWEOIPy6b/hf_20260504_073455_445b3596-744c-4778-bcc6-adbe3e14dec0.png",
        ["Wispr-Flow"],
        [(200,112),(400,225)],
    ),
}


def download(url: str) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read()


def main():
    print(f"Installing {len(TILES)} generated tiles...\n")
    written = 0
    for slug, (url, basenames, sizes) in TILES.items():
        print(f"  {slug:18} ", end="", flush=True)
        png_bytes = download(url)
        # archive original PNG
        (GEN / f"{slug}.png").write_bytes(png_bytes)
        img = Image.open(BytesIO(png_bytes)).convert("RGB")
        # full-size webp(s)
        for base in basenames:
            out = IMAGES / f"{base}.webp"
            img.save(out, "WEBP", quality=90, method=6)
            written += 1
        # resized variants
        for w, h in sizes:
            for base in basenames:
                out = IMAGES / f"{base}-{w}x{h}.webp"
                img.resize((w, h), Image.LANCZOS).save(out, "WEBP", quality=88, method=6)
                written += 1
        print(f"OK ({len(basenames) + len(sizes)*len(basenames)} sizes)")
    print(f"\n=== Wrote {written} webp files ===")


if __name__ == "__main__":
    main()
