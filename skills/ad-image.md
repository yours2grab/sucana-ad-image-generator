# Ad Image Generator

**Triggers:** `ad image`, `/ad-image`, `generate ad`, `create ad image`, `ad image generator`

## Project Root
All files for this skill live at:
`/Users/virgilbrewster/My Drive/Sucana/Sucana/Sucana Agents/Ad Image Generator/`

When reading or writing any file, always use this absolute path as the base.

This skill generates ad images end-to-end. Claude handles all steps autonomously.

## Workflow

### Step 1 — Greet & Path Selection

Start with EXACTLY this (no additions, no preamble):

> "Let's create some magic. How do you want to create an image?
> 1. From your hook and angle?
> 2. From a cool idea you have?
> 3. From a reference image?"

Wait for their answer before doing anything else.

### Step 2 — User Provides Content

**Option 1 (Hook and angle):** Ask: "Paste your hook (and body/CTA if you have them)." Hook alone is enough. Body and CTA are optional. Wait for response.

**Option 2 (Cool idea):** Ask them to describe the idea. Wait for response. If the idea doesn't mention a specific person (gender, age, role, or situation), ask: "Who's in the image and what are they feeling?" Otherwise move on.

**Option 3 (Reference image):** Extract ONLY from the reference image: shot type, aesthetic, format treatment, angle, framing. Do NOT extract: setting, environment, clothing, story. The reference = HOW to shoot. User = WHAT to shoot. Then ask: "What's the ad about? If you have a hook, paste it too."

Wait for response.

### Step 3 — Research

Run research silently for all paths. Never show research output to the user.

**1. Extract keywords:** From the hook, idea, or ad description, pull 3-5 pain-related keywords (e.g., "burnout," "overwhelmed," "behind on deadlines").

**2. Search the Reddit CSV:**
File: `/Users/virgilbrewster/My Drive/Sucana/automations/Reddit-Monitoring/latest-scrape.csv`
Search the Title, Content, and Keywords columns for your extracted keywords. Pull real language, real frustrations, real scenes people describe.

**3. If the CSV is missing, has no matches, or matches are only tangentially related (not about the specific pain in the hook):** Fall back to web search. Search for Reddit threads about the pain point (e.g., `site:reddit.com "burnout" "can't keep up"`). Pull the same thing: real words, real frustrations, real scenes from actual people.

**4. How research shapes the image:** Use what you find to inform three specific prompt fields:
- `mood` — match the emotional tone of real posts (e.g., "defeated" not just "sad")
- `subject.action` — ground the subject in a real moment people described (e.g., "staring at a screen with 47 open tabs")
- `setting.location` — use real environments from the posts (e.g., "home office at 11pm" not generic "office")

**Meta Ad Library:** Not offered by default. Only activates if the user explicitly says "also check Meta" or "research Meta ads."

### Step 4 — Pick a Style

Show ALL frameworks as a numbered list. User picks a number and we move. No explanation needed, no analysis shown.

> "Pick a style:
> 1. Hook Shot — person in a pain moment, editorial, the hook IS the image
> 2. Testimonial — person with a quote or endorsement overlaid
> 3. UGC Selfie — raw phone selfie, zero polish, awkward angle
> 4. POV — shot from the person's perspective (hands on keyboard, phone screen)
> 5. Text Wall — text dominates the frame, person/scene as background
> 6. B-Roll + Text — environment or scene shot with text overlay, no person focus
> 7. Before/After — contrast moment, the pain state before the solution
> 8. Social Proof — person with numbers, reviews, or screenshots overlaid
> 9. Greenscreen — person in foreground, relevant context as background
> 10. Founder — founder/authority portrait with a direct message"

Wait for their number.

### Step 5 — Story Header

After all Q&A is done, write a short creative brief as a heading. One line that captures what you're about to create.

Example: **"Burned-out media buyer, rainy street at night, UGC selfie. The hook hits on surrender."**

This gives the user a preview before any image is generated. Then move straight to generation.

### Step 6 — Generate ONE Master Image

**ONE image. ONE API call. All formats come from this single master.**

Build 1 JSON prompt at **9:16 (1080x1920)** — the tallest format. This is the master image. All other sizes will be cropped from it. Read `skills/nano_banana_image.md` for the full schema.

**Claude picks the subject** — gender, ethnicity, age, clothing. Vary each time.

**Composition rule for master:** The key subject (face, hands, main object) MUST be centered in the middle third of the frame vertically. This ensures every crop (square, landscape, feed) keeps the subject visible.

Generate 1 master image:
```bash
cd "/Users/virgilbrewster/My Drive/Sucana/Sucana/Sucana Agents/Ad Image Generator"
python3 scripts/generate.py "prompts/[subdirectory]/YYYY-MM-DD_style-type_hook-slug_1080x1920.json" --count 1
```

Then crop the master to 1:1 (1080x1080) for preview using `--resize`:
```bash
python3 scripts/generate.py "prompts/[subdirectory]/YYYY-MM-DD_style-type_hook-slug_1080x1080.json" --resize "images/[subdirectory]/YYYY-MM-DD_style-type_hook-slug_1080x1920.png"
```

Show the 1:1 preview to the user. Then ask:
> "Like it or regenerate?"

### Step 7 — Image Approval

- **Approved (like it)** — move to Step 8
- **Rejected (regenerate)** — user says what to fix → update the 9:16 master JSON prompt → regenerate 1 master image → crop to 1:1 preview → show again → repeat until approved

### Step 8 — Crop Master to All 3 Sizes (clean, no text)

**Do NOT call the API again.** Each API call produces a different image. All sizes come from the ONE approved 9:16 master.

**3 formats only. No landscape. No 1200x1200.**

| Size | Ratio | Resolution |
|------|-------|------------|
| Story | 9:16 | 1080x1920 (master) |
| Square | 1:1 | 1080x1080 |
| Feed | 4:5 | 1080x1350 |

Build JSON prompts for the 2 additional sizes (only `ad_format.ratio_and_resolution` changes). Crop the master to each:
```bash
cd "/Users/virgilbrewster/My Drive/Sucana/Sucana/Sucana Agents/Ad Image Generator"
python3 scripts/generate.py "prompts/[sub]/YYYY-MM-DD_style_slug_1080x1080.json" --resize "images/[sub]/YYYY-MM-DD_style_slug_1080x1920.png"
python3 scripts/generate.py "prompts/[sub]/YYYY-MM-DD_style_slug_1080x1350.json" --resize "images/[sub]/YYYY-MM-DD_style_slug_1080x1920.png"
```

After ALL sizes created, build `images/review.html` — dark-background grid with all 3 clean images. Each clickable (opens full size in new tab). Open automatically with `open "images/review.html"`.

### Step 9 — Text Question

> "Want text on the image?"

- **No** → skip to Step 11. Deliver the 3 clean formats.
- **Yes** → ask: "What text? Paste the exact line."
  - Spell-check every word character by character
  - Flag any suspected typo: "Found possible spelling issue: [word]. Did you mean [correction]?"
  - Wait for confirmation
  - If user rewrites the text, use the new version
  - Move to Step 9b

### Step 9b — Generate 6 Images (3 formats × 2 crop options)

After text confirmed:

1. **Back up** all 3 clean images to `images/[subdirectory]/clean/` (create dir if needed)

2. **Create TWO versions per format** from the same master using `--resize` with `--bias`:

   **Option A: Text with space** (offset crop — subject pushed down, text breathes in sky/open space):
   ```bash
   python3 scripts/generate.py "prompts/[sub]/..._1080x1080.json" --resize "images/[sub]/..._1080x1920.png" --bias 0.30
   python3 scripts/generate.py "prompts/[sub]/..._1080x1350.json" --resize "images/[sub]/..._1080x1920.png" --bias 0.30
   ```
   Copy the master 9:16 as-is (no crop needed for story).
   Save A versions with `_textA` suffix before the extension.

   **Option B: Text on face** (center crop — text goes straight over the subject):
   ```bash
   python3 scripts/generate.py "prompts/[sub]/..._1080x1080.json" --resize "images/[sub]/..._1080x1920.png" --bias 0.50
   python3 scripts/generate.py "prompts/[sub]/..._1080x1350.json" --resize "images/[sub]/..._1080x1920.png" --bias 0.50
   ```
   Copy the master 9:16 as-is.
   Save B versions with `_textB` suffix.

3. **Apply bold text overlay** to all 6 images using `--text-only` (add `text_overlay` to JSON prompts first).

4. **Build review.html** showing A and B side by side per format (6 images, 3 rows, 2 columns). Open automatically.

**Crop bias reference:**
| Format | Option A (text space) | Option B (text on face) |
|--------|----------------------|------------------------|
| 9:16 story | Full master (no crop) | Full master (no crop) |
| 1:1 square | --bias 0.30 | --bias 0.50 |
| 4:5 feed | --bias 0.30 | --bias 0.50 |

### Step 10 — User Picks A or B

> "Which style, A or B?"

User picks one. Delete the other set. Keep the chosen 3 images as the final text versions.

If rejected entirely: ask what to fix, restore clean backups from `images/[subdirectory]/clean/`, adjust crop bias or text, regenerate the 6 options.

### Step 10b — Text Variations

> "Want different text on the same image?"

- **No** → Step 11
- **Yes** → user provides new text line:
  1. Restore clean images from `images/[subdirectory]/clean/`
  2. Re-crop with the CHOSEN style (A or B) bias values
  3. Apply new bold text overlay
  4. Show in review.html
  5. If user wants to keep: copy the 3 images to `images/[subdirectory]/text-v[N]/`
  6. Repeat for more text lines
  7. Final review.html shows all kept variations grouped by text line

### Step 11 — Final

Ask: "Want to generate another concept or are we done?"

If another concept → go back to Step 4 (pick a style).

## Aesthetic Rules per Style

### 1. Hook Shot (editorial)
- `aesthetic_style`: "Shot on Sony A7 with 80mm lens. Cinematic teal-orange color grade — blue-pushed shadows, warm protected skin tones. Real environment, real clutter, real people softly blurred in background. Shallow depth of field. Skin pores visible, individual stubble hairs visible. Subject caught mid-thought, NOT posed. Looks like a still from a prestige documentary or drama series."
- `authenticity_level`: `editorial`
- Lens: `80mm`, aperture: `f/2.8`, shallow DOF

### 2. Testimonial (editorial)
- Same editorial aesthetic as Hook Shot
- Composition leaves clear space for quote text
- Person looking confident/relieved (post-solution emotion)
- `authenticity_level`: `editorial`

### 3. UGC Selfie
- `aesthetic_style`: "Shot on iPhone front-facing camera held at arm's length. Slightly awkward angle — not centered, not level. Harsh available light — sunlight through a window, overhead fluorescent, whatever is there. Never beautiful, never controlled. Grainy sensor noise. No post-processing, no color grade. Natural white balance. Real environment clutter in background. Subject caught mid-expression, mid-word — not posed. Looks like a raw selfie video still from TikTok or Instagram Reels."
- `authenticity_level`: `raw_ugc`
- Lens: `50mm equivalent`, aperture: `f/8.0`, wide DOF
- Negative prompt MUST include: `"8K"`, `"ultra realistic"`, `"professional photography"`, `"studio lighting"`, `"cinematic"`, `"CGI"`, `"rendered"`, `"smooth skin"`, `"airbrushed"`, `"perfect framing"`, `"centered composition"`, `"color graded"`, `"posed"`

### 4. POV
- `aesthetic_style`: "Shot on iPhone rear camera, wide angle. Looking down at hands, keyboard, phone screen, or desk. First-person perspective — no face visible. Harsh available light, sensor noise, no color grade. Natural white balance. Real environment clutter. Looks like someone snapped a photo of what's in front of them."
- Shot from the person's perspective (hands on keyboard, phone screen, desk)
- Lens: `28mm equivalent` (iPhone wide), aperture: `f/1.8`, wide DOF
- `authenticity_level`: `raw_ugc`
- Negative prompt MUST include same UGC negatives as Style 3

### 5. Text Wall (editorial)
- Person or scene darkened/blurred as background
- Text fills 60-70% of the frame
- Bold, high-contrast typography
- `authenticity_level`: `editorial`

### 6. B-Roll + Text (editorial)
- Environment/scene shot, no person focus needed
- 35mm wide, f/5.6
- `authenticity_level`: `editorial`

### 7. Before/After (editorial)
- Person in the "before" pain state
- Same editorial aesthetic as Hook Shot
- `authenticity_level`: `editorial`

### 8. Social Proof (editorial)
- Person with review/numbers composited
- Same editorial aesthetic as Hook Shot
- `authenticity_level`: `editorial`

### 9. Greenscreen (editorial)
- Person in foreground, relevant context as background
- 80mm, f/2.8
- `authenticity_level`: `editorial`

### 10. Founder (editorial)
- Authority portrait, direct to camera
- 85mm, f/2.0
- `authenticity_level`: `editorial`

## Universal Rules — enforce on every single image

PERSON
- Every image must feature a person — no exceptions (except Style 4: POV and Style 6: B-Roll + Text)
- Never cartoon, never illustrated, never CGI, never rendered — unless explicitly asked
- Never AI-glossy, never airbrushed, never smooth skin — pores, sweat, texture, realness

COMPOSITION & FRAMING
- Eyes always land on the upper third of the frame
- Always leave headspace above the head — never crop the top
- Never cut in flesh
- Shot types:
  - **Extreme close-up**: from above eyebrows to chin with breathing room below
  - **Close-up**: head to neck
  - **Small medium**: head with headspace down to below the nipples
  - **Full medium**: head to hip
  - **Wide**: full body with environment

TYPOGRAPHY (text overlay path only)
- Text is applied AFTER image generation via Pillow post-processing in generate.py
- **Nike "I'm not Nike" bold style ONLY.** No thin fonts. No subtitles. No Apple style.
- Bold/black font weight (Arial Black, Impact), top-left anchor, stacked lines
- No subtitles, no secondary text lines. Bold headline only.
- Two CROP options when text is added (user picks A or B):
  - **A: Text with space** — offset crop (--bias 0.30), subject pushed down, text breathes in open space
  - **B: Text on face** — center crop (--bias 0.50), text goes straight over the subject
- Aspect-aware line wrapping: portrait max_chars=12, square max_chars=15

FORMATS
- **3 formats only. No landscape. No 1200x1200. No exceptions.**
- Story 9:16 (1080x1920) = master
- Square 1:1 (1080x1080) = crop from master
- Feed 4:5 (1080x1350) = crop from master

IMAGE GENERATION
- Images without text: add `"text"`, `"words"`, `"letters"`, `"writing"`, `"signage"` to negative prompt
- Images with text: text is added by Pillow AFTER generation, so still add text-related terms to negative prompt to keep the base image clean

FILE NAMING
`YYYY-MM-DD_style-type_hook-slug_WxH.json` — take up to the first 4 words of the hook or idea, lowercase, hyphened, special characters stripped. Style-type mapping: hook-shot, testimonial, ugc-selfie, pov, text-wall, b-roll-text, before-after, social-proof, greenscreen, founder. Example: `2026-03-12_ugc-selfie_its-time-to-surrender_1080x1080.json`

SUBDIRECTORIES
- Hook Shot → `prompts/people/`
- Testimonial → `prompts/people/`
- UGC Selfie → `prompts/people/`
- POV → `prompts/people/`
- Text Wall → `prompts/photography/`
- B-Roll + Text → `prompts/photography/`
- Before/After → `prompts/people/`
- Social Proof → `prompts/people/`
- Greenscreen → `prompts/people/`
- Founder → `prompts/people/`

ERROR HANDLING
If generate.py fails (safety filter, rate limit, API error): read the error output, adjust the prompt, save the updated JSON, and retry once. If it fails again, tell the user what went wrong and ask how to proceed.
