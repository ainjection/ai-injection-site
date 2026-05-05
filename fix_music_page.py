#!/usr/bin/env python3
"""Three things on the music page:
1. Rewrite aishotstudio.com .wav URLs to local audio/ folder.
2. Replace Suno affiliate invite link with clean suno.com.
3. Neutralize remaining visible aishotstudio.com links (downloads, author, root)
   so the rebranded page doesn't refer users back to the source site.
"""
import re, sys
from pathlib import Path

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path("C:/Users/clawb/Desktop/claudeclaw-main/site-clones/aishotstudio-full")
PAGES = ROOT / "pages"

WAV_RE = re.compile(
    r'https?://aishotstudio\.com/wp-content/uploads/\d{4}/\d{2}/([A-Za-z0-9._-]+\.(?:wav|mp3|m4a|ogg|flac))(\?[^"\'\s>]*)?',
    re.IGNORECASE,
)
SUNO_AFFILIATE = re.compile(r'https?://suno\.com/invite/@aishotstudio[^"\'\s>]*', re.IGNORECASE)
# Visible link patterns to neutralize on the music page
AISHOT_DOWNLOAD = re.compile(r'https?://aishotstudio\.com/download/[^"\'\s>]+', re.IGNORECASE)
AISHOT_AUTHOR   = re.compile(r'https?://aishotstudio\.com/author/[^"\'\s>]+', re.IGNORECASE)
AISHOT_ROOT     = re.compile(r'href="https?://aishotstudio\.com/?"', re.IGNORECASE)


def fix_music():
    page = PAGES / "music" / "raw.html"
    audio_dir = PAGES / "music" / "audio"
    local_audio = {p.name for p in audio_dir.iterdir() if p.is_file()}

    html = page.read_text(encoding="utf-8", errors="ignore")
    n_wav = n_suno = n_dl = n_auth = n_root = 0

    # 1. wav URLs → local
    def wav_repl(m):
        nonlocal n_wav
        fn = m.group(1)
        suffix = m.group(2) or ""
        if fn in local_audio:
            n_wav += 1
            return f"audio/{fn}{suffix}"
        return m.group(0)
    html = WAV_RE.sub(wav_repl, html)

    # 2. Suno affiliate → clean
    html, n_suno = SUNO_AFFILIATE.subn("https://suno.com", html)

    # 3. Visible aishotstudio.com links → safe targets
    # Download links go to the local music page anchor (they were per-track downloads)
    html, n_dl = AISHOT_DOWNLOAD.subn("#", html)
    # Author link → drop to '#'
    html, n_auth = AISHOT_AUTHOR.subn("#", html)
    # Root link → AI Injection home
    html, n_root = AISHOT_ROOT.subn('href="../home/raw.html"', html)

    page.write_text(html, encoding="utf-8")
    print(f"  wav URLs localized:        {n_wav}")
    print(f"  Suno affiliate cleaned:    {n_suno}")
    print(f"  Download links neutralized:{n_dl}")
    print(f"  Author links neutralized:  {n_auth}")
    print(f"  Root link → AI Injection:  {n_root}")


if __name__ == "__main__":
    fix_music()
