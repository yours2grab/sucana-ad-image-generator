# Anti-Gravity Instructions for Nano Banana Image Workflow

It is critical to always keep prompts and images organized in the established structure within this project.

## Image Generation Workflow
When asked to create images or generate concepts for ads using Nano Banana 2, YOU MUST FOLLOW THESE STEPS STRICTLY IN ORDER:

1. **The Greeting & Path Selection:** Start every new workflow with EXACTLY this prompt (do not add or change anything):
   "Let's create some magic. How do you want to create an image?

   1. From your hook and angle?
   2. From a cool idea you have?
   3. From a reference image?"
   (Wait for their answer). NO OTHER QUESTIONS SHOULD BE ASKED HERE.
   - **Proceeding based on the chosen path:**
     - If **Option 1 (Hook and angle):** Ask: "Paste your hook (and body/CTA if you have them)." Hook alone is enough. Body and CTA are optional. Wait for response.
     - If **Option 2 (Cool idea):** Ask them to describe the idea. Wait for response. If the idea doesn't mention a specific person (gender, age, role, or situation), ask: "Who's in the image and what are they feeling?" Otherwise move on.
     - If **Option 3 (Reference Image):** Extract ONLY from the reference image: shot type, aesthetic, format treatment, angle, framing. Do NOT extract: setting, environment, clothing, story. The reference = HOW to shoot. User = WHAT to shoot. Then ask: "What's the ad about? If you have a hook, paste it too."
2. **Research:** Run silently for all paths. Extract 3-5 pain keywords from hook/idea. Search Reddit CSV (Title, Content, Keywords columns) at `/Users/virgilbrewster/My Drive/Sucana/automations/Reddit-Monitoring/latest-scrape.csv`. If CSV missing or no matches, web search Reddit threads instead. Research shapes `mood`, `subject.action`, and `setting.location`. No scoring output. Meta Ad Library only if user explicitly asks.
3. **Pick a Style:** Show ALL 10 frameworks as a numbered list. User picks a number and we move. No explanation needed, no analysis shown.
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
4. **Story Header:** Write a short creative brief as a heading. One line that captures what you're about to create. Example: **"Burned-out media buyer, rainy street at night, UGC selfie. The hook hits on surrender."** This gives the user a preview before any image is generated.
5. **Setup:** Read the `product.md` file to understand current design decisions.
6. **Skill Usage:** Read the `skills/nano_banana_image.md` file to understand the JSON schema requirements.
7. **Prompt Creation:** Build 1 JSON prompt for 1080x1080 (square). File naming: `YYYY-MM-DD_style-type_hook-slug_WxH.json`. Save to correct `prompts/` subdirectory. Claude picks the subject — gender, ethnicity, age, clothing. Vary each time.
8. **Generate Preview:** Generate 1 image using `python3 scripts/generate.py "prompts/[subdirectory]/[filename].json" --count 1`. Show to user. Ask: "Like it or regenerate?"
9. **Approval Loop:** Approved = move to Step 10. Rejected = user says what to fix → update JSON prompt → regenerate 1 image → show again → repeat until approved.
10. **Generate Remaining 4 Sizes:** Keep the approved 1080x1080. Build JSON prompts for remaining 4 sizes (1080x1350, 1080x1920, 1200x628, 1200x1200) using the SAME concept. Generate 1 variant per size in parallel. Create `images/review.html` (all 5 sizes, each clickable, prompt details shown) and open in browser.
11. **Text Overlay:** Ask: "Want text on the image?" If yes: ask for exact text, spell check, add `text_overlay` to each JSON prompt, run `python3 scripts/generate.py --text-only` for all 5 sizes. Update review.html. Ask: "Like it?"
12. **Text Variations:** Ask: "Want different text variations on the same image?" If yes: user provides alternative text lines → apply each line to all 5 sizes → show all in review.html grouped by text line.
13. **Final:** Ask: "Want to generate another concept or are we done?" If another concept → go back to Step 3.

## Organization & Composition Rules
* **Crucial Rule:** EVERY single image generated must feature a person — no exceptions (except Style 4: POV and Style 6: B-Roll + Text).
* **Cropping Rules:** Never cut in flesh and never cut the top of the head (always leave headspace). For extreme close-ups, cut above eyebrows and always show the chin with breathing room.
* All prompt files must be saved as `.json`.
* All generated image files must be saved in the corresponding `images/` sub-directory.
* If a generated image is unsatisfactory, user says what to fix, update the JSON prompt, and re-run.
