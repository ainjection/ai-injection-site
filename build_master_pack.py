#!/usr/bin/env python3
"""Combine all prompt collections from the site into one HTML file styled
to AI Injection brand. The HTML is then rendered to PDF by render_pdf.py.
"""
import html as html_lib
import re, sys
from pathlib import Path

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path("C:/Users/clawb/Desktop/claudeclaw-main/site-clones/aishotstudio-full")
PAGES = ROOT / "pages"
OUT_HTML = ROOT / "lead-magnet" / "ai-injection-master-prompt-pack.html"
OUT_HTML.parent.mkdir(exist_ok=True)

# Order matters — controls table of contents
SECTIONS = [
    ("42-camera-movements",          "42 Camera Movements",       "Every camera movement with copy-paste prompt for AI video generation."),
    ("27-cinematic-looks-lighting",  "27 Cinematic Looks",         "Lighting setups for cinematic AI shots."),
    ("26-camera-angles-shot-types",  "26 Camera Angles & Shot Types", "Composition prompts for any AI video tool."),
    ("46-song-genres",               "46 Song Genres for Suno",    "Music genre prompt structure for Suno and other AI music generators."),
    ("viral-video-transitions",      "Viral Video Transitions",    "Transition prompts for short-form video."),
    ("text-to-video-prompt-structure","Text-to-Video Prompt Structure", "How to structure prompts that work."),
    ("16-ai-image-generators",       "16 AI Image Generators",     "Comparison and prompts for the best AI image tools."),
    ("elevenlabs-audio-tags",        "ElevenLabs Audio Tags",      "Voice and emotion tags for AI speech synthesis."),
]


def clean_markdown(md: str) -> str:
    """Strip junk lines and aishotstudio.com noise from the scraped markdown."""
    lines = []
    for line in md.splitlines():
        s = line.strip()
        if not s:
            lines.append("")
            continue
        # skip image markdown, skip-to-content links, author bylines, brand links
        if s.startswith("[!["):
            continue
        if "Skip to content" in s or "awb-open-oc" in s:
            continue
        if "AIShotStudio" in s and ("author" in s or "Posts by" in s):
            continue
        if re.fullmatch(r'\[!\[.*\]\(.*\)\]\(.*\)', s):
            continue
        if re.fullmatch(r'\[.*\]\(https?://aishotstudio\.com/[^\)]*\)', s):
            # standalone link to aishotstudio – usually nav/header
            continue
        # rewrite any aishotstudio.com mentions in body text → AI Injection
        s = re.sub(r'aishotstudio\.com', 'aiinjection.com', s, flags=re.IGNORECASE)
        s = re.sub(r'AI ?Shot ?Studio', 'AI Injection', s)
        lines.append(s)
    return "\n".join(lines)


def md_to_html(md: str) -> str:
    """Minimal markdown→HTML for headings, paragraphs, code, and lists.

    Every text fragment is HTML-escaped before being placed in tags so that
    scraped markdown can't smuggle <script>, raw HTML, or unbalanced tags into
    the final document.
    """
    def esc(s: str) -> str:
        return html_lib.escape(s, quote=False)

    out = []
    in_list = False
    for raw in md.splitlines():
        line = raw.rstrip()
        if not line:
            if in_list:
                out.append("</ul>"); in_list = False
            continue
        # heading
        m = re.match(r'^(#{1,6})\s+(.*)$', line)
        if m:
            if in_list:
                out.append("</ul>"); in_list = False
            level = len(m.group(1))
            text = esc(m.group(2))
            out.append(f"<h{level}>{text}</h{level}>")
            continue
        # bullet
        if line.startswith("- ") or line.startswith("* "):
            if not in_list:
                out.append("<ul>"); in_list = True
            out.append(f"<li>{esc(line[2:])}</li>")
            continue
        # paragraph
        if in_list:
            out.append("</ul>"); in_list = False
        out.append(f"<p>{esc(line)}</p>")
    if in_list:
        out.append("</ul>")
    return "\n".join(out)


def main():
    sections_html = []
    toc_items = []
    for slug, title, subtitle in SECTIONS:
        md_path = PAGES / slug / "page.md"
        if not md_path.exists():
            print(f"  ! missing {md_path}")
            continue
        md = md_path.read_text(encoding="utf-8", errors="ignore")
        clean = clean_markdown(md)
        # Drop the original H1 — we replace it with our section title
        clean = re.sub(r'^#\s+.*$', '', clean, count=1, flags=re.MULTILINE)
        body = md_to_html(clean)
        anchor = slug
        toc_items.append(f'<li><a href="#{anchor}">{title}</a> <span class="muted">— {subtitle}</span></li>')
        sections_html.append(f"""
<section id="{anchor}" class="page-break">
  <div class="section-header">
    <span class="section-badge">{title.split()[0]}</span>
    <h1 class="section-title">{title}</h1>
    <p class="section-subtitle">{subtitle}</p>
  </div>
  <div class="section-body">
{body}
  </div>
</section>""")

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>AI Injection — Master Prompt Pack</title>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&family=JetBrains+Mono:wght@400;600&display=swap" rel="stylesheet">
<style>
  @page {{ size: A4; margin: 18mm 16mm; }}
  * {{ box-sizing: border-box; }}
  body {{
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    color: #1a1a35;
    background: #ffffff;
    line-height: 1.55;
    margin: 0;
    font-size: 11pt;
  }}
  .cover {{
    page-break-after: always;
    background: linear-gradient(135deg, #0F0F23 0%, #1a1140 60%, #2a0f5e 100%);
    color: #ffffff;
    padding: 80px 60px;
    min-height: 95vh;
    display: flex;
    flex-direction: column;
    justify-content: center;
    position: relative;
    overflow: hidden;
  }}
  .cover::before {{
    content: '';
    position: absolute;
    top: -50px; right: -50px;
    width: 400px; height: 400px;
    background: radial-gradient(circle, rgba(0,212,255,0.4) 0%, transparent 70%);
    filter: blur(20px);
  }}
  .cover::after {{
    content: '';
    position: absolute;
    bottom: -100px; left: -100px;
    width: 500px; height: 500px;
    background: radial-gradient(circle, rgba(139,92,246,0.4) 0%, transparent 70%);
    filter: blur(30px);
  }}
  .cover-eyebrow {{
    font-size: 13pt;
    letter-spacing: 0.3em;
    color: #00D4FF;
    font-weight: 700;
    margin-bottom: 24px;
    text-transform: uppercase;
    position: relative;
  }}
  .cover h1 {{
    font-size: 56pt;
    font-weight: 900;
    line-height: 1.05;
    margin: 0 0 24px;
    letter-spacing: -0.02em;
    background: linear-gradient(135deg, #00D4FF 0%, #ffffff 50%, #8B5CF6 100%);
    -webkit-background-clip: text;
    background-clip: text;
    color: transparent;
    position: relative;
  }}
  .cover-tagline {{
    font-size: 16pt;
    color: rgba(255,255,255,0.85);
    max-width: 560px;
    line-height: 1.4;
    position: relative;
  }}
  .cover-stats {{
    display: flex;
    gap: 40px;
    margin-top: 48px;
    position: relative;
  }}
  .cover-stat {{ }}
  .cover-stat-num {{
    font-size: 42pt;
    font-weight: 800;
    color: #00D4FF;
    text-shadow: 0 0 20px rgba(0,212,255,0.6);
    line-height: 1;
  }}
  .cover-stat-label {{
    font-size: 10pt;
    color: rgba(255,255,255,0.7);
    text-transform: uppercase;
    letter-spacing: 0.15em;
    margin-top: 6px;
  }}
  .cover-footer {{
    position: absolute;
    bottom: 40px; left: 60px; right: 60px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-size: 9pt;
    color: rgba(255,255,255,0.6);
  }}
  .cover-brand {{
    font-weight: 800;
    letter-spacing: 0.2em;
    color: #00D4FF;
  }}

  .toc {{
    page-break-after: always;
    padding: 40px 30px;
  }}
  .toc h2 {{
    font-size: 24pt;
    color: #0F0F23;
    border-bottom: 3px solid #00D4FF;
    padding-bottom: 10px;
    margin-bottom: 24px;
  }}
  .toc ul {{
    list-style: none;
    padding-left: 0;
  }}
  .toc li {{
    padding: 10px 0;
    border-bottom: 1px solid #eee;
    font-size: 11pt;
  }}
  .toc a {{
    color: #1a1a35;
    text-decoration: none;
    font-weight: 600;
  }}
  .toc .muted {{ color: #888; font-weight: 400; }}

  section.page-break {{ page-break-before: always; padding: 30px; }}
  .section-header {{
    margin-bottom: 28px;
    padding-bottom: 16px;
    border-bottom: 2px solid #00D4FF;
  }}
  .section-badge {{
    display: inline-block;
    padding: 4px 12px;
    background: linear-gradient(135deg, #00D4FF, #8B5CF6);
    color: white;
    font-size: 9pt;
    font-weight: 800;
    border-radius: 12px;
    letter-spacing: 0.1em;
    margin-bottom: 8px;
  }}
  .section-title {{
    font-size: 28pt;
    font-weight: 800;
    margin: 0 0 8px;
    color: #0F0F23;
    letter-spacing: -0.02em;
  }}
  .section-subtitle {{
    color: #555;
    font-size: 11pt;
    margin: 0;
  }}
  .section-body h2 {{
    font-size: 16pt;
    color: #0F0F23;
    margin-top: 28px;
    margin-bottom: 12px;
    border-left: 4px solid #00D4FF;
    padding-left: 12px;
  }}
  .section-body h3 {{
    font-size: 12.5pt;
    color: #1a1a35;
    margin-top: 18px;
    margin-bottom: 6px;
    font-weight: 700;
  }}
  .section-body h4, .section-body h5, .section-body h6 {{
    font-size: 11pt;
    margin-top: 14px;
    margin-bottom: 4px;
  }}
  .section-body p {{
    margin: 6px 0 12px;
    color: #2a2a45;
  }}
  .section-body ul {{ margin: 6px 0 14px 20px; }}
  .section-body li {{ margin: 4px 0; }}

  .footer-cta {{
    page-break-before: always;
    background: linear-gradient(135deg, #0F0F23 0%, #1a1140 100%);
    color: white;
    padding: 80px 60px;
    text-align: center;
    min-height: 95vh;
    display: flex;
    flex-direction: column;
    justify-content: center;
  }}
  .footer-cta h2 {{
    font-size: 32pt;
    font-weight: 900;
    margin: 0 0 16px;
    background: linear-gradient(135deg, #00D4FF, #8B5CF6);
    -webkit-background-clip: text;
    background-clip: text;
    color: transparent;
  }}
  .footer-cta p {{
    font-size: 14pt;
    color: rgba(255,255,255,0.85);
    max-width: 540px;
    margin: 0 auto 32px;
    line-height: 1.4;
  }}
  .footer-cta .cta-btn {{
    display: inline-block;
    background: linear-gradient(135deg, #00D4FF, #8B5CF6);
    color: #0F0F23;
    font-weight: 800;
    padding: 16px 40px;
    border-radius: 32px;
    text-decoration: none;
    font-size: 13pt;
    box-shadow: 0 0 40px rgba(0,212,255,0.5);
  }}
  .footer-cta .cta-url {{
    margin-top: 16px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 10pt;
    color: #00D4FF;
  }}
</style>
</head>
<body>

<div class="cover">
  <div class="cover-eyebrow">AI Injection · Master Pack v1</div>
  <h1>Every<br>AI Prompt<br>You'll Need.</h1>
  <p class="cover-tagline">The complete library of camera movements, lighting setups, shot types, music genres, transitions and prompt structures for AI video, image, and music generation. One file. Yours forever.</p>
  <div class="cover-stats">
    <div class="cover-stat">
      <div class="cover-stat-num">200+</div>
      <div class="cover-stat-label">prompts</div>
    </div>
    <div class="cover-stat">
      <div class="cover-stat-num">8</div>
      <div class="cover-stat-label">collections</div>
    </div>
    <div class="cover-stat">
      <div class="cover-stat-num">$0</div>
      <div class="cover-stat-label">forever</div>
    </div>
  </div>
  <div class="cover-footer">
    <span class="cover-brand">AI INJECTION</span>
    <span>aiinjection.com · Skool community: skool.com/ai-injection-4241</span>
  </div>
</div>

<div class="toc">
  <h2>What's Inside</h2>
  <ul>
{chr(10).join(toc_items)}
  </ul>
</div>

{''.join(sections_html)}

<div class="footer-cta">
  <h2>Want Weekly New Prompts + Live Workshops?</h2>
  <p>Join the AI Injection Skool community. 1,000+ creators sharing what works in AI video, image, and music. New prompts every week. Workshops, breakdowns, and the templates that actually convert.</p>
  <a class="cta-btn" href="https://www.skool.com/ai-injection-4241">Join AI Injection Skool — Free</a>
  <div class="cta-url">skool.com/ai-injection-4241</div>
</div>

</body>
</html>
"""
    OUT_HTML.write_text(html, encoding="utf-8")
    print(f"Wrote {OUT_HTML} ({len(html):,} chars)")


if __name__ == "__main__":
    main()
