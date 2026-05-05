# AIShotStudio — Full Site Clone

Captured 2026-05-03. Full-site mirror of aishotstudio.com for portfolio template reference.

## Stats
- **Pages captured:** 27 (this folder) + 1 (`../aishotstudio-music/`) = **28 total**
- **Markdown lines:** 4,519
- **Images downloaded:** 584
- **Total size:** 92 MB

## Capture Method
- **Tier 1 (6 high-value prompt pages) + Tier 2 hubs (3):** Firecrawl scrape (markdown + raw HTML + full-page screenshot + image links + branding tokens)
- **Tier 2 remainder + Tier 3 + Tier 4 (18 pages):** curl + MarkItDown (Firecrawl credits depleted at page 9; switched to local pipeline — same output minus screenshots, equivalent for content extraction)

## Folder structure per page
```
pages/<slug>/
  page.md              # clean markdown
  raw.html             # original HTML for layout reference
  clean.html           # sanitized HTML (Firecrawl pages only)
  screenshot.png       # full-page screenshot (Firecrawl pages only)
  metadata.json        # title, description, og tags
  image-urls.json      # all unique image URLs found on the page
  images/              # downloaded images (capped at 50 per page)
```

## Tier 1 — Core prompt collections (Firecrawl, full quality)
- `42-camera-movements/` — every camera movement with copy-paste prompt
- `27-cinematic-looks-lighting/` — 27 lighting setups
- `26-camera-angles-shot-types/` — 26 shot types
- `46-song-genres/` — 46 music genres for Suno (911 lines, biggest catalogue)
- `viral-video-transitions/`
- `text-to-video-prompt-structure/`

## Tier 2 — Hub pages
- `home/` — homepage card grid (Firecrawl)
- `shot-design/` — Shot Design hub (Firecrawl)
- `prompt-library/` — Prompt Library hub (Firecrawl)
- `ai-toolset/` — AI Toolset directory (curl)
- `learn-ai/` — Learn AI page (curl)

## Tier 3 — Specialized prompt pages (curl)
- `still-camera-fix/`
- `true-360-180-orbit/`
- `higgsfield-camera-comparison/`
- `higgsfield-focal-length/`
- `higgsfield-aperture/`
- `16-ai-image-generators/`
- `elevenlabs-audio-tags/`
- `technical-portrait-poses/`
- `gender-swap-prompts/`
- `character-actor-catwalk/`
- `border-break-master/`

## Tier 4 — Meta-prompt examples (curl)
- `lacoste-crocodile-seedance/`
- `morning-rush-seedance/`
- `volleyball-freeze-seedance/`
- `phone-catch-seedance/`
- `cockroaches-bed/`

## Already-captured separately
- `../aishotstudio-music/` — /music page (audio library + track metadata in `extracted/tracks.json`)
- `~/.claude/skills/prank-reel/SKILL.md` — `/why-you-so-obsessed-with-me-meta-prompt` page captured as a usable skill

## Branding tokens (from /music/ Firecrawl pull)
- Primary: `#1E293B` (dark slate)
- Accent: `#D344FA` (vibrant magenta)
- Background: `#030303` (near-black)
- Heading font: **Heebo** · Body: Arial/Helvetica fallback
- Border radius: `4px` · Base unit: `4px`
- Layout system: 2-column card grid on dark bg, full-width hero, footer with logo/links

## Skipped (legal / taxonomy)
- /privacy-policy /cookie-policy /disclaimer /terms-of-service
- /links /category/random-prompts
