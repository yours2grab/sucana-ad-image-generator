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
> 10. Founder — founder/authority portrait with a direct message
> 11. Data vs Reality — person centered, contrasting stats on left vs right (what the platform said vs what actually happened)"

Wait for their number.

### Step 5 — Story Header

After all Q&A is done, write a short creative brief as a heading. One line that captures what you're about to create.

Example: **"Burned-out media buyer, rainy street at night, UGC selfie. The hook hits on surrender."**

This gives the user a preview before any image is generated. Then move straight to generation.

### Step 6 — Generate ONE Master Image

**ONE image. ONE API call. All formats come from this single master.**

**HARD RULE: ALWAYS use Nano Banana MCP for image generation. NEVER use generate.py for generation. NEVER use Gemini Flash. generate.py is ONLY for local cropping (--resize) and text overlay (--text-only).**

Build 1 JSON prompt at **9:16 (1080x1920)** — the tallest format. This is the master image. All other sizes will be cropped from it. Read `skills/nano_banana_image.md` for the full schema.

**HARD RULE: ALL questions to the user must be numbered options (1, 2, 3, etc.). Never ask open-ended questions. The user types a number and we move.**

**Step 6-pre — Subject Selection (5 options, user picks):**

Before generating anything, present EXACTLY 5 subject options. Each option must be a different person — vary gender, ethnicity, age, and setting. Write each as a short one-liner describing who they are and what they're doing.

Example format:
> "Who's in the shot?
> 1. Woman, late 20s, Black, messy bun, staring at laptop in a dark bedroom
> 2. Man, mid 40s, white, reading glasses pushed up on forehead, kitchen table at midnight
> 3. Woman, early 30s, East Asian, oversized hoodie, slumped in an office chair
> 4. Man, late 20s, Latino, backwards cap, rubbing his eyes at a standing desk
> 5. Non-binary, mid 30s, South Asian, headphones around neck, two monitors glowing"

Always vary across gender, ethnicity, age, and environment. Never repeat the same type twice. Wait for the user to pick a number.

**Composition rule for master:** The key subject (face, hands, main object) MUST be centered in the middle third of the frame vertically. This ensures every crop (square, landscape, feed) keeps the subject visible.

**Step 6a — Generate master via Nano Banana MCP:**

1. Save the JSON prompt to `prompts/[subdirectory]/YYYY-MM-DD_style-type_hook-slug_1080x1920.json`
2. Build the full text prompt from the JSON (same format as build_prompt in generate.py)
3. Call `mcp__plugin_creative_nano-banana__generate_image` with:
   - `prompt`: the full text prompt
   - `aspectRatio`: "9:16"
4. Copy the generated image from Nano Banana's output path to the correct location:
   ```bash
   cp "[nano-banana-output-path]" "/Users/virgilbrewster/My Drive/Sucana/Sucana/Sucana Agents/Ad Image Generator/images/[subdirectory]/YYYY-MM-DD_style-type_hook-slug_1080x1920.png"
   ```

**Step 6b — Crop to 1:1 preview (local, no API):**
```bash
cd "/Users/virgilbrewster/My Drive/Sucana/Sucana/Sucana Agents/Ad Image Generator"
python3 scripts/generate.py "prompts/[subdirectory]/YYYY-MM-DD_style-type_hook-slug_1080x1080.json" --resize "images/[subdirectory]/YYYY-MM-DD_style-type_hook-slug_1080x1920.png"
```

**Step 6c — Build review.html and open it immediately.** Do NOT just show the image in chat. Always build `images/review.html` with a dark background grid and open it with `open "images/review.html"` so the user sees it full-size in their browser.

Then ask:
> "1. Like it
> 2. Regenerate"

### Step 7 — Image Approval

- **1 (like it)** — move to Step 8
- **2 (regenerate)** — ask: "What do you want different?" Wait for answer → update the 9:16 master JSON prompt → regenerate 1 master image via Nano Banana MCP (NEVER generate.py) → copy to images/ → crop to 1:1 preview → build review.html → open → ask "1. Like it  2. Regenerate" again

### Step 8 — Crop Master to All 3 Sizes (clean, no text)

**Do NOT call the API again.** Each API call produces a different image. All sizes come from the ONE approved 9:16 master.

**4 formats.**

| Size | Ratio | Resolution | Source |
|------|-------|------------|--------|
| Story | 9:16 | 1080x1920 | Master (generated via Nano Banana) |
| Square | 1:1 | 1080x1080 | Crop from master |
| Feed | 4:5 | 1080x1350 | Crop from master |
| Landscape | 1.91:1 | 1200x628 | **Separate generation via Nano Banana at 16:9** |

**HARD RULE: Landscape is NEVER cropped from the 9:16 master. Portrait-to-landscape crop destroys quality. Landscape is ALWAYS generated separately via Nano Banana MCP at 16:9 aspect ratio using the same prompt adapted for landscape.**

**Step 8a — Crop Square and Feed from master (local, no API):**
```bash
cd "/Users/virgilbrewster/My Drive/Sucana/Sucana/Sucana Agents/Ad Image Generator"
python3 scripts/generate.py "prompts/[sub]/YYYY-MM-DD_style_slug_1080x1080.json" --resize "images/[sub]/YYYY-MM-DD_style_slug_1080x1920.png"
python3 scripts/generate.py "prompts/[sub]/YYYY-MM-DD_style_slug_1080x1350.json" --resize "images/[sub]/YYYY-MM-DD_style_slug_1080x1920.png"
```

**Step 8b — Generate Landscape separately via Nano Banana:**
1. Build JSON prompt for 1200x628 (same subject/setting/mood, `ad_format.ratio_and_resolution` = "Landscape (1.91:1) 1200x628")
2. Call `mcp__plugin_creative_nano-banana__generate_image` with `aspectRatio: "16:9"` and the full text prompt
3. Copy the generated image to `images/[sub]/YYYY-MM-DD_style_slug_1200x628.png`

After ALL 4 sizes ready, build `images/review.html` — dark-background grid with all 4 clean images. Each clickable (opens full size in new tab). Open automatically with `open "images/review.html"`.

### Step 9 — Text Question

> "1. No text, deliver clean
> 2. Add text"

- **1** → skip to Step 11. Deliver the 3 clean formats.
- **2** → ask: "Paste the exact text line."
  - Spell-check every word character by character
  - Flag any suspected typo: "Found possible spelling issue: [word]. Did you mean [correction]?"
  - Wait for confirmation
  - If user rewrites the text, use the new version
  - Move to Step 9b

### Step 9b — Generate 8 Images (4 formats × 2 crop options)

After text confirmed:

1. **Back up** all 4 clean images to `images/[subdirectory]/clean/` (create dir if needed)

2. **Create TWO versions per format** from the same master using `--resize` with `--bias`:

   **Option A: Text with space** (offset crop — subject pushed down, text breathes in sky/open space):
   ```bash
   python3 scripts/generate.py "prompts/[sub]/..._1080x1080.json" --resize "images/[sub]/..._1080x1920.png" --bias 0.30
   python3 scripts/generate.py "prompts/[sub]/..._1080x1350.json" --resize "images/[sub]/..._1080x1920.png" --bias 0.30
   python3 scripts/generate.py "prompts/[sub]/..._1200x628.json" --resize "images/[sub]/..._1080x1920.png" --bias 0.30
   ```
   Copy the master 9:16 as-is (no crop needed for story).
   Save A versions with `_textA` suffix before the extension.

   **Option B: Text on face** (center crop — text goes straight over the subject):
   ```bash
   python3 scripts/generate.py "prompts/[sub]/..._1080x1080.json" --resize "images/[sub]/..._1080x1920.png" --bias 0.50
   python3 scripts/generate.py "prompts/[sub]/..._1080x1350.json" --resize "images/[sub]/..._1080x1920.png" --bias 0.50
   python3 scripts/generate.py "prompts/[sub]/..._1200x628.json" --resize "images/[sub]/..._1080x1920.png" --bias 0.50
   ```
   Copy the master 9:16 as-is.
   Save B versions with `_textB` suffix.

3. **Apply bold text overlay** to all 8 images using `--text-only` (add `text_overlay` to JSON prompts first).

4. **Build review.html** showing A and B side by side per format (8 images, 4 rows, 2 columns). Open automatically.

**Crop bias reference:**
| Format | Option A (text space) | Option B (text on face) |
|--------|----------------------|------------------------|
| 9:16 story | Full master (no crop) | Full master (no crop) |
| 1:1 square | --bias 0.30 | --bias 0.50 |
| 4:5 feed | --bias 0.30 | --bias 0.50 |
| 1.91:1 landscape | --bias 0.30 | --bias 0.50 |

### Step 10 — User Picks A or B

> "1. Style A (text with space)
> 2. Style B (text on face)
> 3. Reject both, start over"

- **1** — delete B set. Keep A as final text versions.
- **2** — delete A set. Keep B as final text versions.
- **3** — ask what to fix, restore clean backups from `images/[subdirectory]/clean/`, adjust crop bias or text, regenerate the 6 options.

### Step 10b — Text Variations

> "1. Done with text
> 2. Try different text on same image"

- **1** → Step 11
- **2** → ask: "Paste the new text line." User provides new text:
  1. Restore clean images from `images/[subdirectory]/clean/`
  2. Re-crop with the CHOSEN style (A or B) bias values
  3. Apply new bold text overlay
  4. Show in review.html
  5. If user wants to keep: copy the 3 images to `images/[subdirectory]/text-v[N]/`
  6. Repeat for more text lines
  7. Final review.html shows all kept variations grouped by text line

### Step 11 — Final

> "1. Another concept
> 2. Done"

- **1** → go back to Step 4 (pick a style).
- **2** → wrap up.

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
- **ABSOLUTE HARD RULE — NO PHONE. EVER.** A phone must NEVER appear in a UGC Selfie image. Not in the person's hand. Not at the edge of frame. Not as a reflection. Not as a prop. NEVER. The selfie FEEL comes ONLY from imperfect framing: tilted 5-10 degrees off level, slightly off-center, angle slightly too high or too low, composition feels accidental. That's it. No phone. No arm holding a phone. No device of any kind. Just a person's face/upper body with imperfect framing that feels like "I took this myself." THE PHONE IS INVISIBLE BECAUSE IT IS THE CAMERA.
- `aesthetic_style`: "Shot on iPhone front-facing camera. Frame tilted 5-10 degrees off level. Slightly off-center. Angle a little too high or too low. Composition feels accidental, like someone held a phone and snapped without thinking. Harsh available light — sunlight through a window, overhead fluorescent, whatever is there. Never beautiful, never controlled. Grainy sensor noise. No post-processing, no color grade. Natural white balance. Real environment clutter in background. Subject caught mid-expression, mid-word — not posed. Looks like a raw selfie video still from TikTok or Instagram Reels."
- `authenticity_level`: `raw_ugc`
- Lens: `50mm equivalent`, aperture: `f/8.0`, wide DOF
- Negative prompt MUST include: `"8K"`, `"ultra realistic"`, `"professional photography"`, `"studio lighting"`, `"cinematic"`, `"CGI"`, `"rendered"`, `"smooth skin"`, `"airbrushed"`, `"perfect framing"`, `"centered composition"`, `"color graded"`, `"posed"`, `"mirror selfie"`, `"phone"`, `"smartphone"`, `"mobile phone"`, `"cellphone"`, `"holding phone"`, `"phone in hand"`, `"phone screen"`, `"device"`, `"selfie arm"`, `"arm extended"`, `"hand holding device"`

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

### 11. Data vs Reality (editorial)
- `aesthetic_style`: "Person centered in frame, looking defeated/frustrated. Left side shows platform-reported stats (green arrows, big numbers). Right side shows reality stats (red arrows, small numbers). Split composition with person as the emotional anchor in the middle. Clean data visualization style, not cluttered. Dark or muted background so the stats pop. Feels like a dashboard exposé."
- Person centered, contrasting data on left vs right
- Left = what the platform/dashboard claimed (inflated numbers, green, up arrows)
- Right = what actually happened (real numbers, red, down arrows)
- Same editorial aesthetic as Hook Shot for the person
- 80mm, f/2.8
- `authenticity_level`: `editorial`
- Text overlay on this style is the STATS, not a headline. Pillow applies the left/right stat layout after generation.
- Negative prompt MUST include: `"text"`, `"words"`, `"letters"` (stats are added via Pillow post-processing, keep base image clean)

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
- **4 formats.**
- Story 9:16 (1080x1920) = master (Nano Banana)
- Square 1:1 (1080x1080) = crop from master
- Feed 4:5 (1080x1350) = crop from master
- Landscape 1.91:1 (1200x628) = **separate generation via Nano Banana at 16:9** (NEVER crop from portrait master)

IMAGE GENERATION
- **ALWAYS use Nano Banana MCP (`mcp__plugin_creative_nano-banana__generate_image`) for ALL image generation. NEVER use generate.py for generation. NEVER use Gemini Flash or Imagen API directly.**
- **generate.py is ONLY for local operations: cropping (--resize), text overlay (--text-only). These do NOT call any API.**
- After Nano Banana generates an image, ALWAYS copy it from the Nano Banana output path to the correct `images/[subdirectory]/` location before proceeding
- Images without text: add `"text"`, `"words"`, `"letters"`, `"writing"`, `"signage"` to negative prompt
- Images with text: text is added by Pillow AFTER generation, so still add text-related terms to negative prompt to keep the base image clean

FILE NAMING
`YYYY-MM-DD_style-type_hook-slug_WxH.json` — take up to the first 4 words of the hook or idea, lowercase, hyphened, special characters stripped. Style-type mapping: hook-shot, testimonial, ugc-selfie, pov, text-wall, b-roll-text, before-after, social-proof, greenscreen, founder, data-vs-reality. Example: `2026-03-12_ugc-selfie_its-time-to-surrender_1080x1080.json`

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
- Data vs Reality → `prompts/people/`

ERROR HANDLING
If Nano Banana MCP fails (safety filter, rate limit, API error): read the error output, adjust the prompt, save the updated JSON, and retry once. If it fails again, tell the user what went wrong and ask how to proceed. If generate.py fails on a local operation (--resize or --text-only), check the file paths and retry.
