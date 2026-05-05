# AI Injection — Static Site

Static clone of the AI Injection site, deployed to Cloudflare Pages.

## Local development

```bash
# Serve from project root
python -m http.server 8765

# Visit
http://127.0.0.1:8765/pages/home/raw.html
```

## Pages

- `pages/home/raw.html` — landing page
- `pages/prompt-library/raw.html` — prompt library index
- `pages/ai-toolset/raw.html` — AI tools showcase
- `pages/ai-influencer-prompts/raw.html` — AI influencer prompts gallery
- `pages/nano-banana-json/raw.html` — Nano Banana 2 JSON prompts
- ... (~30 sub-pages)

## Build & maintenance scripts

| Script | Purpose |
|---|---|
| `compress_assets.py` | PNG→WebP-85, WAV→MP3-192, rewrite HTML refs, delete originals |
| `inject_link_fix.py` | Add lightbox + click-interceptor for legacy aishotstudio.com links |
| `build_obsessed_page.py` | Build the local "Why You So Obsessed With Me" prompt page |

## Deploy

Cloudflare Pages auto-deploys on every push to `main`.
