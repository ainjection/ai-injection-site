"""Compress all local PNG/JPG images to WebP-85, WAV→MP3-192, and rewrite
all HTML src/href references in one pass. Idempotent: skips files with an
existing optimized sibling."""
import json, re, subprocess, sys
from pathlib import Path
from PIL import Image, ImageFile

ImageFile.LOAD_TRUNCATED_IMAGES = True
ROOT = Path(__file__).parent
PAGES = ROOT / "pages"
QUALITY = 85
MIN_BYTES = 50_000  # don't bother compressing files smaller than 50 KB
MAPPING = {}  # original_path → new_path (relative to ROOT)

def relpath(p: Path):
    return str(p.relative_to(ROOT)).replace("\\", "/")

def compress_image(p: Path):
    if p.suffix.lower() not in {".png", ".jpg", ".jpeg"}:
        return None
    if p.stat().st_size < MIN_BYTES:
        return None
    out = p.with_suffix(".webp")
    if out.exists() and out.stat().st_mtime >= p.stat().st_mtime:
        return None  # already converted
    try:
        with Image.open(p) as im:
            if im.mode in ("RGBA", "LA"):
                pass
            elif im.mode != "RGB":
                im = im.convert("RGB")
            im.save(out, "WEBP", quality=QUALITY, method=6)
        return (relpath(p), relpath(out))
    except Exception as e:
        print(f"  ! failed {p.name}: {e}")
        return None

def compress_audio(p: Path):
    if p.suffix.lower() != ".wav":
        return None
    out = p.with_suffix(".mp3")
    if out.exists() and out.stat().st_mtime >= p.stat().st_mtime:
        return None
    try:
        subprocess.run(
            ["ffmpeg", "-y", "-i", str(p), "-c:a", "libmp3lame", "-b:a", "192k",
             "-loglevel", "error", str(out)],
            check=True, capture_output=True
        )
        return (relpath(p), relpath(out))
    except Exception as e:
        print(f"  ! audio failed {p.name}: {e}")
        return None

def main():
    print("Step 1: compressing images and audio...")
    n_img = n_aud = 0
    for p in PAGES.rglob("*"):
        if not p.is_file(): continue
        m = compress_image(p)
        if m:
            MAPPING[m[0]] = m[1]
            n_img += 1
            if n_img % 50 == 0:
                print(f"  ...{n_img} images")
        m = compress_audio(p)
        if m:
            MAPPING[m[0]] = m[1]
            n_aud += 1
    print(f"  Done: {n_img} images, {n_aud} audio.")

    # Save mapping as JSON for debug
    (ROOT / "_compress_map.json").write_text(
        json.dumps(MAPPING, indent=2), encoding="utf-8"
    )

    print("\nStep 2: rewriting src/href in HTML files...")
    n_html = 0
    n_replacements = 0
    for html in PAGES.rglob("*.html"):
        txt = html.read_text(encoding="utf-8", errors="ignore")
        new = txt
        for old_rel, new_rel in MAPPING.items():
            # Match by filename (handles relative paths like "images/foo.png" or "../images/foo.png")
            old_name = old_rel.rsplit("/", 1)[-1]
            new_name = new_rel.rsplit("/", 1)[-1]
            if old_name in new:
                new = new.replace(old_name, new_name)
                n_replacements += new.count(new_name) - txt.count(new_name)
        if new != txt:
            html.write_text(new, encoding="utf-8")
            n_html += 1
    # Also update the root index.html if any
    for html in [ROOT / "index.html"]:
        if not html.exists(): continue
        txt = html.read_text(encoding="utf-8", errors="ignore")
        new = txt
        for old_rel, new_rel in MAPPING.items():
            old_name = old_rel.rsplit("/", 1)[-1]
            new_name = new_rel.rsplit("/", 1)[-1]
            if old_name in new:
                new = new.replace(old_name, new_name)
        if new != txt:
            html.write_text(new, encoding="utf-8")
            n_html += 1
    print(f"  Done: {n_html} HTML files updated.")

    print("\nStep 3: deleting original heavyweight files...")
    deleted_bytes = 0
    n_del = 0
    for old_rel in MAPPING.keys():
        p = ROOT / old_rel
        if p.exists():
            sz = p.stat().st_size
            p.unlink()
            deleted_bytes += sz
            n_del += 1
    print(f"  Deleted {n_del} originals, freed {deleted_bytes/1024/1024:.1f} MB")

    print("\nDone.")

if __name__ == "__main__":
    main()
