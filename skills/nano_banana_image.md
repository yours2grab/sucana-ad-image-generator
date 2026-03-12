# Nano Banana Image Generation Skill

Use this skill whenever you need to translate natural language image descriptions into precise, structured instructions for the Imagen 4.0 image model.

## Why JSON Prompting?
Computers and AI models process JSON (JavaScript Object Notation) highly efficiently. By structuring the prompt into distinct, explicitly defined JSON arguments, we prevent the model from misinterpreting vague textual combinations, ensuring significantly higher consistency, adherence to style, and precise control over elements like lighting, camera angle, and composition.

## The JSON Prompt Schema

When the user asks you to generate a prompt, always output the prompt following this exact JSON structure:

```json
{
  "subject": {
    "description": "Specific details about the main focus of the image (age, gender, ethnicity, clothing, pose, facial expression, skin texture). Be hyper-specific — no vague descriptors.",
    "action": "What the subject is currently doing, described as a present-tense action."
  },
  "setting": {
    "location": "The environment or background. Tie this explicitly to the hook and emotional tone.",
    "time_of_day": "Morning, noon, golden hour, dusk, night — be specific."
  },
  "composition": {
    "camera_angle": "Eye-level, low angle, high angle, extreme close-up, medium shot, wide shot.",
    "framing": "Rule of thirds or centered. MUST follow cropping rules: never cut in flesh, always leave headspace (no cutting top of head), for extreme close-ups cut above eyebrows and always show chin with breathing room."
  },
  "camera_settings": {
    "lens": "80mm for portraits, 35mm for environment-heavy shots, 50mm for medium.",
    "aperture": "f/2.8 for subject-focused portraits, f/4.0 for wider, f/8.0 for UGC/phone-style.",
    "depth_of_field": "shallow | medium | wide",
    "motion_blur": "none | subtle"
  },
  "lighting": {
    "type": "Natural light, soft window light, phone screen glow, harsh fluorescent, golden hour sun — be specific to the setting.",
    "color_grading": "Cool tones, warm amber, high contrast, desaturated, vintage film grain, cinematic teal-orange."
  },
  "mood": "The explicit emotional tone of the image — exhausted, frustrated, focused, determined, raw, anxious. This is the feeling the viewer should immediately sense.",
  "authenticity_level": "editorial | raw_ugc — defines how polished or unpolished the aesthetic should feel.",
  "aesthetic_style": "Full aesthetic description. For editorial: cinematic teal-orange, Sony A7. For UGC: shot-on-phone, grainy, no color grade.",
  "ad_format": {
    "platform": "Ad image",
    "ratio_and_resolution": "Specific size, e.g. Square (1:1) 1080x1080"
  },
  "negative_prompt": [
    "text",
    "watermarks",
    "logos",
    "bad anatomy",
    "deformities",
    "extra fingers",
    "blurry face",
    "3D render",
    "cartoon",
    "illustration",
    "stock photo look",
    "overly polished",
    "fake smile"
  ],
  "text_overlay": {
    "text": "Optional. The exact text to overlay on the image after generation.",
    "placement": "clean_separation | deliberate_cut_through"
  }
}
```

## Universal Sizes — Always Generate All 5

| Size | Ratio | Resolution |
|------|-------|------------|
| Square | 1:1 | 1080x1080 |
| Feed | 4:5 | 1080x1350 |
| Story | 9:16 | 1080x1920 |
| Landscape | 1.91:1 | 1200x628 |
| Large Square | 1:1 | 1200x1200 |

Preview image is always 1080x1080. After approval, generate remaining 4 sizes.

## HARD RULES — Enforced on Every Single Image, No Exceptions

### SHOT TAXONOMY — Exact Cut Points
Every prompt MUST specify one of these. No vague "close-up" or "medium shot" — use these exact definitions:

| Shot Type | Cut Points |
|-----------|-----------|
| **Extreme Close-Up** | Top frame: above eyebrows. Bottom frame: chin with breathing room below. Nothing else. |
| **Close-Up** | Top frame: crown with headspace. Bottom frame: base of neck. |
| **Small Medium** | Top frame: crown with headspace. Bottom frame: below the nipples. |
| **Full Medium** | Top frame: crown with headspace. Bottom frame: hip. |
| **Wide** | Full body visible. Environment fills the frame. Subject is part of the world, not the world. |

**Cropping rules — non-negotiable:**
- Eyes ALWAYS land in the upper third of the frame
- ALWAYS leave headspace above the head — never crop the crown
- NEVER cut in flesh — no cuts at joints (neck, shoulder, wrist, knee, hip). Cut above or below, never through
- Bottom frame always has breathing room — never tight to the chin or feet

---

### MICRO EXPRESSIONS — The Face Must Tell the Whole Story
Generic emotions are banned. "Frustrated", "tired", "happy" — these are not prompts, they're useless.

Every image MUST specify the exact micro expression: the specific muscle, the specific moment, the specific involuntary tell.

**Examples of correct micro expression prompting:**
- "Jaw slightly dropped, lower lip barely parted — the half-second before words form. Eyes slightly widened, upper eyelids raised, pupils tracking left — processing something he didn't expect."
- "Corners of the mouth pulled back, not up — the grimace of someone swallowing bad news. Brow slightly furrowed, one side higher than the other. Nostrils barely flared."
- "Eyes mid-blink, caught between closed and open — the exhaustion blink, not the alert blink. Chin slightly dropped toward chest. Shoulders rounded forward."
- "One eyebrow raised higher than the other. Lips pressed together — the held-breath moment before responding. Neck muscles visible under skin."
- "Upper lip curled asymmetrically on one side — disbelief without surprise. Eyes narrowed slightly, focused hard on something off-frame."

The micro expression is what makes viewers stop scrolling. It must feel involuntary, caught, real — NOT performed for a camera.

For UGC especially: micro expressions are the difference between an image that looks like an ad and one that looks like a real person having a real moment.

---

### CINEMATIC vs UGC — Two Completely Different Worlds

#### CINEMATIC (editorial styles: Hook Shot, Testimonial, Text Wall, B-Roll, Before/After, Social Proof, Greenscreen, Founder)
Intentional. Controlled. Every frame choice is deliberate.
- Camera is steady, placed with purpose
- Angle is chosen by a director who knows exactly what they're doing
- Composition is tight — rule of thirds, precise headspace, exact framing
- Color grade is active — teal-orange push, blue shadows, warm skin tones
- Depth of field is shallow and deliberate — background bokeh is smooth, intentional
- Lighting is real but shaped — window light, practical lamp, controlled bounce
- The subject does NOT know they're being photographed. Caught mid-thought, mid-action.
- Feels like a still from a prestige drama or documentary series

#### UGC — Shot Like an Idiot Grabbed Their Phone (UGC Selfie, POV)
This is NOT cinematic. This is NOT controlled. This is someone who does not know how to take a photo.
- **Angle is wrong** — phone held slightly too high, slightly too low, tilted 5–10 degrees off level. NEVER straight, NEVER centered
- **Framing is off** — subject slightly left or right of center. Part of a shoulder cut. Slightly too much ceiling. Accidentally bad composition.
- **Light is whatever was there** — harsh window sun blasting half the face, fluorescent overhead casting ugly shadows, phone screen glow from below. No one moved the light.
- **Grip is awkward** — slight motion blur from hand instability. You can feel the arm holding the phone.
- **No color grade** — raw phone white balance, slightly cool or slightly orange depending on the room. No post.
- **Grain and sensor noise** — visible, especially in shadows
- **Subject is mid-something** — mid-word, mid-expression, mid-breath. NOT posed. NOT held. NOT ready.
- The whole thing looks like evidence, not content.

**Negative prompt for UGC MUST include:** `"8K"`, `"ultra realistic"`, `"professional photography"`, `"studio lighting"`, `"cinematic"`, `"CGI"`, `"rendered"`, `"smooth skin"`, `"airbrushed"`, `"perfect framing"`, `"centered composition"`, `"color graded"`, `"posed"`, `"intentional composition"`, `"rule of thirds"`

---

## The 10 Style Frameworks

### Default camera for editorial styles
**80mm lens, f/2.8 aperture, shallow depth of field. Shot on Sony A7 or equivalent cinema camera. Cinematic teal-orange color grade — blue-pushed shadows, warm protected skin tones. Subject caught in a genuine moment — NOT posed, NOT looking at camera unless the concept explicitly requires it. Real environment with real people softly blurred in background. Skin pores visible, individual stubble hairs visible. Looks like a still from a prestige documentary or drama series.** Apply these to every editorial concept without exception.

### 1. Hook Shot (editorial)
Direct visual of the hook. The scene makes the hook obvious at a glance — no interpretation required. Person in a pain moment, the hook IS the image.
- `authenticity_level`: `editorial`
- Lens: 80mm, f/2.8, shallow DOF
- Subject and setting drawn directly from the hook's words

### 2. Testimonial (editorial)
Person with a quote or endorsement overlaid. Same editorial aesthetic as Hook Shot.
- `authenticity_level`: `editorial`
- Composition leaves clear space for quote text
- Person looking confident/relieved (post-solution emotion)

### 3. UGC Selfie (raw_ugc)
Someone grabbed their phone and filmed themselves. That's it. The imperfection IS the power — awkward angle, harsh light, zero polish. MUST NOT look professional in any way.
- `authenticity_level`: `raw_ugc`
- Lens: 50mm equivalent (phone front camera), f/8.0, wide depth of field
- Phone held at arm's length — slightly off-center, not level, slightly tilted
- Harsh available light, grain, sensor noise, zero color grading
- Subject caught mid-expression, mid-word — never posed
- `aesthetic_style`: `"Shot on iPhone front-facing camera held at arm's length. Slightly awkward angle — not centered, not level. Harsh available light with no diffusion. Grainy sensor noise. No post-processing, no color grade. Natural white balance. Real environment clutter in background. Subject caught mid-expression, mid-word — not posed. Looks like a raw selfie video still from TikTok or Instagram Reels."`
- **Vary subject gender and environment every time**
- Negative prompt MUST include: `"8K"`, `"ultra realistic"`, `"professional photography"`, `"studio lighting"`, `"cinematic"`, `"CGI"`, `"rendered"`, `"smooth skin"`, `"airbrushed"`, `"perfect framing"`, `"centered composition"`, `"color graded"`, `"posed"`

### 4. POV (raw_ugc)
Shot from the person's perspective. Hands on keyboard, phone screen, looking down at desk. No face visible — this is an exception to the "every image must have a person" rule.
- `authenticity_level`: `raw_ugc`
- iPhone, wide angle
- Real environment, real clutter

### 5. Text Wall (editorial)
Text dominates the frame. Person or scene darkened/blurred as background.
- `authenticity_level`: `editorial`
- Text fills 60-70% of the frame
- Bold, high-contrast typography

### 6. B-Roll + Text (editorial)
Environment/scene shot with text overlay. No person focus needed — exception to the person rule.
- `authenticity_level`: `editorial`
- 35mm wide, f/5.6

### 7. Before/After (editorial)
Person in the "before" pain state. Contrast moment. Same editorial aesthetic as Hook Shot.
- `authenticity_level`: `editorial`
- Lens: 80mm, f/2.8, shallow DOF

### 8. Social Proof (editorial)
Person with numbers, reviews, or screenshots overlaid. Same editorial aesthetic as Hook Shot.
- `authenticity_level`: `editorial`
- Lens: 80mm, f/2.8, shallow DOF

### 9. Greenscreen (editorial)
Person in foreground, relevant context as background.
- `authenticity_level`: `editorial`
- 80mm, f/2.8

### 10. Founder (editorial)
Authority portrait, direct to camera. Founder/expert with a direct message.
- `authenticity_level`: `editorial`
- 85mm, f/2.0

## Workflow Execution Steps

1. **Path Selection:** Ask exactly one question — hook/angle, cool idea, or reference image. Wait for reply.
2. **Research:** Silent. Reddit CSV → web search fallback. Shapes mood, action, setting.
3. **Style Selection:** Show all 10 frameworks as numbered list. User picks a number.
4. **Story Header:** One-line creative brief before generation.
5. **Prompt Creation:** Build 1 JSON prompt for 1080x1080. Assign hyper-specific values to every key. Do not leave any key empty. Save to correct `prompts/` subdirectory. File naming: `YYYY-MM-DD_style-type_hook-slug_WxH.json`.
6. **Preview Generation:** Generate 1 image at 1080x1080. Show to user. Ask: "Like it or regenerate?"
7. **Approval:** Iterate until approved.
8. **Full Generation:** Keep approved 1080x1080. Generate remaining 4 sizes with same concept. Create review.html.
9. **Text Overlay:** After all sizes done, ask about text. Apply via `--text-only` flag.
10. **Text Variations:** Optional — different text lines on same images.
11. **Final:** Another concept or done?
