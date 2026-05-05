#!/usr/bin/env python3
"""Wire each "Download" button on the music page to the right audio file by
matching it with the nearest preceding <audio src="audio/...wav"> tag.

Also adds the `download` HTML attribute so the browser saves the file rather
than streaming it inline, and points the link directly at the .wav.
"""
import re, sys
from pathlib import Path

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

PAGE = Path("C:/Users/clawb/Desktop/claudeclaw-main/site-clones/aishotstudio-full/pages/music/raw.html")

# Find every <audio ... src="audio/SOMETHING.wav?_=N"> in order
AUDIO_RE = re.compile(r'<audio\b[^>]*?\bsrc="(audio/[^"?]+\.wav)(?:\?[^"]*)?"', re.IGNORECASE)

# Find every Download button with href="#" — the empty-href ones we neutralized earlier
# Match an <a ... href="#" ...>...Download...</a>
DOWNLOAD_BTN_RE = re.compile(
    r'<a\b([^>]*?)href="#"([^>]*?)>(\s*<span[^>]*>Download</span>)',
    re.IGNORECASE,
)


def main():
    html = PAGE.read_text(encoding="utf-8", errors="ignore")

    audio_srcs = [(m.start(), m.group(1)) for m in AUDIO_RE.finditer(html)]
    print(f"Found {len(audio_srcs)} audio tracks")
    for pos, src in audio_srcs:
        print(f"  @ pos {pos:6}: {src}")

    # For each Download button, find the latest audio src that appears BEFORE it
    new_html = []
    last = 0
    fixed = 0
    for m in DOWNLOAD_BTN_RE.finditer(html):
        before, attrs_left, attrs_right, span = m.start(), m.group(1), m.group(2), m.group(3)
        # find the most recent audio src before this position
        match_src = None
        for pos, src in audio_srcs:
            if pos < before:
                match_src = src
            else:
                break
        if not match_src:
            continue
        new_html.append(html[last:before])
        # Build new <a ... href="<src>" download ...>
        new_anchor = f'<a{attrs_left}href="{match_src}" download{attrs_right}>{span}'
        new_html.append(new_anchor)
        last = m.end()
        fixed += 1
    new_html.append(html[last:])

    if fixed:
        PAGE.write_text("".join(new_html), encoding="utf-8")
    print(f"\n=== Wired {fixed} Download buttons to local .wav files ===")


if __name__ == "__main__":
    main()
