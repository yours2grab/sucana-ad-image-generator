# Ad Image Generator — Build Manual

## What This Is
A Claude Code skill (`/ad-image`) that takes a hook, angle, idea, or reference image and generates high-quality ad creatives end-to-end. It runs research, lets the user pick from 10 style frameworks, generates a preview image for approval, then expands to all 5 ad sizes, with optional text overlay and text variations.

## Project Structure
- `skills/nano_banana_image.md` — JSON schema and rules for building image prompts
- `prompts/people/` — people-focused prompts (Hook Shot, Testimonial, UGC Selfie, POV, Before/After, Social Proof, Greenscreen, Founder)
- `prompts/photography/` — environment/scene prompts (Text Wall, B-Roll + Text)
- `images/` — generated PNG output, mirroring the prompts folder structure
- `images/examples/captions/` — approved reference images for text-in-image style
- `images/examples/image-only/` — approved reference images for no-text style
- `images/review.html` — browser grid for reviewing all generated variants
- `great-images.md` — curated log of strong outputs worth referencing
- **Image generation script:** `scripts/generate.py`
- **Model:** Imagen 4.0

## Skill File Location
`~/.claude/commands/ad-image.md`

## Design Decisions (March 2026)

### 10 Style Frameworks
1. Hook Shot — person in a pain moment, editorial
2. Testimonial — person with quote overlaid, editorial
3. UGC Selfie — raw phone selfie, zero polish
4. POV — person's perspective (hands, screen, desk)
5. Text Wall — text dominates, person/scene as background
6. B-Roll + Text — environment shot with text overlay
7. Before/After — contrast moment, pain state
8. Social Proof — person with numbers/reviews overlaid
9. Greenscreen — person foreground, context background
10. Founder — authority portrait, direct message

### Typography Placement — Two Modes (never in between)
**A. Clean Separation** — text in negative space beside, above, or around the face. Never touching the face.
**B. Deliberate Cut-Through** — text LARGE and bold, intentionally crossing through forehead or mid-face. Design choice, not accidental.
**NEVER:** awkward overlap, text grazing the edge of a face, text that looks accidentally placed.

Text is applied AFTER image generation via Pillow post-processing in generate.py. Use `--text-only` flag to apply text to existing images without regenerating.

### Platform Sizes
All 5 sizes are always generated. No platform question asked.

| Size | Ratio | Resolution |
|------|-------|------------|
| Square | 1:1 | 1080x1080 |
| Feed | 4:5 | 1080x1350 |
| Story | 9:16 | 1080x1920 |
| Landscape | 1.91:1 | 1200x628 |
| Large Square | 1:1 | 1200x1200 |

### Workflow Order
1. Greet → ask path (hook/angle, cool idea, reference image)
2. User provides content (hook alone is enough, body/CTA optional)
3. Run research (Reddit CSV grep, all paths) — silent, no scoring output
4. Show 10 style frameworks as numbered list → user picks a number
5. Story header — one-line creative brief before generation
6. Generate 1 preview image (1080x1080 square) → show to user
7. Approval: "Like it or regenerate?" → iterate until approved
8. Generate remaining 4 sizes (keep approved 1080x1080) → create review.html → open in browser
9. Ask: "Want text on the image?" → spell check → apply text overlay via `--text-only` → update review.html
10. Ask: "Want different text variations?" → apply each line to all 5 sizes
11. Ask: "Another concept or done?" → loop to Step 4 if another

### Research Stack
- **Step 1:** Extract 3-5 pain keywords from the hook/idea
- **Step 2:** Search Reddit CSV (Title, Content, Keywords columns) at `/Users/virgilbrewster/My Drive/Sucana/automations/Reddit-Monitoring/latest-scrape.csv`
- **Step 3 (fallback):** If CSV missing or no relevant matches, web search Reddit threads about the pain point
- **How research shapes prompts:** Directly informs `mood`, `subject.action`, and `setting.location` in the JSON prompt
- **Meta Ad Library** — hidden option. Only activates if user explicitly says "also check Meta." Not offered by default.
- No scoring output. Research shapes concepts silently.

### Composition Rules (All Images)
- Eyes on the upper third of the frame always
- Always leave headspace — never crop the top of the head
- Never cut in flesh — never cut at neck, shoulder, wrist, hip, waist, or any joint

### Image Quality Standard
- Always hyper-realistic — pores, sweat, stubble, skin texture visible
- Never AI-glossy, never airbrushed, never smooth
- Never cartoon, CGI, illustrated, or rendered unless explicitly asked

### Editorial Aesthetic (Hook Shot, Testimonial, Text Wall, B-Roll, Before/After, Social Proof, Greenscreen, Founder)
- Shot on Sony A7, 80mm, f/2.8, shallow DOF
- Cinematic teal-orange color grade — blue-pushed shadows, warm skin tones
- Subject caught mid-moment, NOT posed, NOT performing
- Real environment clutter in background

### UGC Aesthetic (UGC Selfie, POV)
- iPhone front camera, held at arm's length, slightly awkward angle
- Harsh available light — never beautiful, never controlled
- Grain, no color grade, natural white balance
- Subject mid-expression, mid-word — never posed
- Vary gender and environment every time

### Generation & Review
- Preview: 1 image at 1080x1080 for approval
- Full generation: 1 variant per size, 4 remaining sizes (approved 1080x1080 kept)
- After generation, always create `images/review.html` and open automatically
- review.html: dark background, grouped by size, each clickable, prompt details shown
- Text overlay applied post-generation via `python3 scripts/generate.py --text-only`

### What product.md Is NOT
Not a run log. Not an iteration log. Do not write to it after each image generation session. It is a build manual only — update it only when design decisions change.
