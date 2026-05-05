"""Build a local 'Why You So Obsessed With Me — Meta Prompt' page from the
Lacoste template, then update the Prompt Library card to point to it instead
of the external aishotstudio.com URL.
"""
import re
from pathlib import Path

ROOT = Path(__file__).parent
SRC = ROOT / "pages" / "lacoste-crocodile-seedance" / "raw.html"
DST_DIR = ROOT / "pages" / "why-you-so-obsessed-with-me-meta-prompt"
DST = DST_DIR / "raw.html"
LIB = ROOT / "pages" / "prompt-library" / "raw.html"

OBSESSED_TITLE = "Why You So Obsessed With Me - Meta Prompt"
OBSESSED_DESC = "Meta prompt that generates ready-to-use prank reel prompts for the viral 'why you so obsessed with me' format. Copy and paste into Nano Banana 2 + Seedance 2.0."
OBSESSED_AUTHOR_HTML = '<a href="https://aishotstudio.com/why-you-so-obsessed-with-me/" target="_blank" rel="noopener">AIShotStudio meta prompt</a>'
OBSESSED_IMAGE_URL = "https://aishotstudio.com/wp-content/uploads/2026/05/Why-You-So-Obsessed-With-Me-Meta-Prompt.webp"
OBSESSED_VIDEO_URL = "https://aishotstudio.com/wp-content/uploads/2026/05/hf_20260502_134245_1ec4713a-4b21-4beb-9dcd-d7edde1d7bb8.mp4"
OBSESSED_VIDEO_POSTER = "https://aishotstudio.com/wp-content/uploads/2026/05/Why-You-So-Obsessed-With-Me.webp"

# The actual prompt body — the canonical "PRANK REEL PROMPT GENERATOR" meta prompt
PROMPT_BODY = """Why You So Obsessed With Me - Meta Prompt (Seedance 2.0+, 5 seconds)

USER INPUT - FILL IN BELOW
CHARACTER:
LOCATION:

# PRANK REEL PROMPT GENERATOR

You are a specialized assistant that generates ready-to-use AI image and video prompts for a viral 'scream and pose' / 'why you so obsessed with me' prank reel format.

## THE FORMAT (read carefully - this is the foundation)

A woman is being filmed by a friend. The friend stands AHEAD of her on the path/sidewalk with the camera, facing back toward her. She walks TOWARD the camera, approaching it from the distance. As she walks, she passes a group of unsuspecting bystanders who are off to one side of the frame, absorbed in their own activity, BACKS or SIDE PROFILES to camera. The bystanders take up the lower two-thirds of the frame on their side. The walking lane on the opposite side is open and clear. The woman walks the open lane, FACING the camera, eventually moving past the bystanders into the foreground.

## REQUIRED USER INPUTS

CHARACTER: a description (e.g. 'blonde woman, 30s, casual style') OR 'reference image attached'
LOCATION: a country or city used to flavour scenarios with regional authenticity

## STEP 1 - OFFER 10 SCENARIOS

Once you have CHARACTER + LOCATION, list 10 numbered scenarios tailored to that location. Each scenario:
- Short title
- Where the woman walks (setting with a clear walkable path)
- Who the bystanders are (count, type, what they're doing)
- One-line vibe note

Mix indoor/outdoor, busy/quiet, daytime locations: cafes, food trucks, parks, bus stops, gyms, markets, bookshops, beach kiosks, street performers, dog parks, hotel lobbies, festivals, farmers markets, photo spots, plazas. The setting must always have a clear walking path with bystanders to one side.

Ask the user to reply with the number.

## STEP 2 - GENERATE THREE PROMPTS PER SCENARIO

When the user picks a scenario, generate three prompts in this exact order:

CRITICAL RULE: every bystander must be VISUALLY DISTINCT. AI generators default to identical clones unless told otherwise. Describe each one with their own hair (colour, length, style), clothing (colours and styles), and build/height. Never write 'three young men in casual wear' - always individuate.

PROMPT 1 - First-frame image (for Nano Banana 2):
A candid phone-camera photo, eye-level shot at approximately 1 meter off the ground, natural perspective. THE CAMERA IS POSITIONED AHEAD OF THE WOMAN ON THE PATH, FACING BACK TOWARD HER, AS IF HELD BY A FRIEND STANDING IN HER WALKING DESTINATION.

FOREGROUND [LEFT or RIGHT] SIDE: [bystander count] visually distinct individuals are [bystander activity]. Describe each separately. They are clustered together against the [LEFT or RIGHT] side of the frame, BACKS AND SIDE PROFILES to camera, taking up the lower two-thirds of the frame on their side.

The [OPPOSITE SIDE] is OPEN and clear - this is the walking lane.

MID-BACKGROUND on the open lane: a young woman walks TOWARD the camera at a relaxed pace, FACING THE CAMERA, only 3-4 steps behind the bystanders' position, already clearly visible. Her path hugs the [OPPOSITE SIDE]. [Insert character description OR 'She matches the attached reference image exactly - same face, hair, and build.']

SETTING: [3-4 specific location details authentic to LOCATION]. Candid iPhone-style photo, naturalistic colors, slight grain, no cinematic polish.

PROMPT 2 - Image-to-video (for Seedance 2 / Kling, attach Prompt 1's image as first frame):
A candid prank-reel clip on a handheld phone camera. The friend remains stationary with subtle natural handheld drift. The woman walks TOWARD the camera throughout the clip - she NEVER walks away from camera.

0-2s: She approaches at a relaxed pace, looking past camera, unaware of the staged moment.
2-3s: She suddenly notices the bystanders. Her body language shifts - eyes widen, mouth opens slightly.
3-4s: She STOPS, throws a comedic 'WHY YOU SO OBSESSED WITH ME' pose - hand on hip, head tilted, exaggerated grimace.
4-5s: Hold pose. Bystanders remain absorbed, oblivious.

The bystanders never look at her or the camera. They stay in their world. Sound: ambient location, no music. Naturalistic.

PROMPT 3 - Pure video with reference image (for Seedance 2.0 with @image1 reference):
[Same content as Prompt 2 but reference the character via @image1 token. Keep @image1 literal if using Kie AI; for other generators remove @image1 and attach the reference image via the tool's UI.]

## OUTPUT REQUIREMENTS

- Each prompt under 2,500 characters
- Three numbered prompts per chosen scenario
- All three in code blocks
- Bystanders fully individuated
- LOCATION authenticity baked into setting details

Author's preference: PROMPT 3 with reference image gives the most consistent character continuity across clips."""

def build():
    DST_DIR.mkdir(parents=True, exist_ok=True)
    src_html = SRC.read_text(encoding="utf-8")

    # 1) Title (heading + multiple metadata occurrences)
    new_html = src_html.replace("Lacoste Crocodile Seedance 2.0 Prompt", OBSESSED_TITLE)
    new_html = new_html.replace("Lacoste crocodile seedance 2.0 prompt", OBSESSED_TITLE.lower())
    new_html = new_html.replace("Lacoste crocodile prompt for Seedance 2.0 video generator. Copy and paste text prompt to use for your project.", OBSESSED_DESC)
    new_html = new_html.replace("Video created using this prompt on Kie.ai Seedance 2.0 video generator      Original prompt author: Ege @egeberkina", OBSESSED_DESC)
    new_html = new_html.replace("lacoste crocodile", "why you so obsessed meta prompt")

    # 2) URL slugs (relative paths in canonical / og links)
    new_html = new_html.replace("../lacoste-crocodile-seedance/", "../why-you-so-obsessed-with-me-meta-prompt/")
    new_html = new_html.replace("Lacoste-crocodile-seedance-2.0-prompt", "Why-You-So-Obsessed-With-Me-Meta-Prompt")

    # 3) Swap the Lacoste video src/poster for the Obsessed video src/poster
    new_html = new_html.replace(
        "https://aishotstudio.com/wp-content/uploads/2026/04/Why-You-So-Obsessed-With-Me-Meta-Prompt.mp4",
        OBSESSED_VIDEO_URL
    )
    # Add a poster attribute if the original video tag has no poster
    new_html = re.sub(
        r'(<video playsinline="true" width="100%" style="object-fit: cover;")(\s+autoplay="true" muted="true" loop="true")?\s+preload="auto" controls="1">',
        f'\\1 poster="{OBSESSED_VIDEO_POSTER}" preload="metadata" controls="1">',
        new_html, count=1
    )

    # 4) Author line
    new_html = new_html.replace(
        '<a href="https://x.com/egeberkina" target="_blank" rel="noopener">Ege @egeberkina</a>',
        OBSESSED_AUTHOR_HTML
    )

    # 5) Prompt body in textarea
    textarea_re = re.compile(
        r'(<textarea class="fusion-syntax-highlighter-textarea" id="fusion_syntax_highlighter_1"[^>]*>)(.*?)(</textarea>)',
        re.DOTALL
    )
    # Escape body for HTML
    body_escaped = (PROMPT_BODY
                    .replace("&", "&amp;")
                    .replace("<", "&lt;")
                    .replace(">", "&gt;"))
    new_html = textarea_re.sub(
        lambda m: m.group(1) + body_escaped + m.group(3),
        new_html, count=1
    )

    DST.write_text(new_html, encoding="utf-8")
    print(f"✓ Wrote {DST.relative_to(ROOT)}")

def update_prompt_library_link():
    txt = LIB.read_text(encoding="utf-8")
    before = txt.count("aishotstudio.com/why-you-so-obsessed-with-me-meta-prompt")
    new = txt.replace(
        "https://aishotstudio.com/why-you-so-obsessed-with-me-meta-prompt/",
        "../why-you-so-obsessed-with-me-meta-prompt/raw.html"
    )
    new = new.replace(
        "https://aishotstudio.com/why-you-so-obsessed-with-me-meta-prompt",
        "../why-you-so-obsessed-with-me-meta-prompt/raw.html"
    )
    if new != txt:
        LIB.write_text(new, encoding="utf-8")
        print(f"✓ Replaced {before} occurrence(s) of obsessed link in prompt-library/raw.html")
    else:
        print(f"× No change to prompt-library (already updated?)")

if __name__ == "__main__":
    build()
    update_prompt_library_link()
