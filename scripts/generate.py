import argparse
import base64
import glob
import json
import os
import subprocess
import sys
import time
import requests
from dotenv import load_dotenv
from PIL import Image, ImageDraw, ImageFont

# Load API key from .env file
load_dotenv()
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

if not GEMINI_API_KEY or GEMINI_API_KEY == "your_api_key_here":
    print("Error: Please add your GEMINI_API_KEY to the .env file.")
    sys.exit(1)

IMAGEN_URL = "https://generativelanguage.googleapis.com/v1beta/models/imagen-4.0-generate-001:predict"

ASPECT_RATIO_MAP = {
    "1:1": "1:1",
    "4:5": "3:4",
    "9:16": "9:16",
    "1.91:1": "16:9",
}

# 4 formats. All cropped from the 9:16 master.
# Story:     1080x1920 (9:16) — master
# Square:    1080x1080 (1:1)
# Feed:      1080x1350 (4:5)
# Landscape: 1200x628  (1.91:1)

def get_aspect_ratio(resolution_string):
    # Check longer keys first to avoid substring false matches (e.g. "1:1" matching "1.91:1")
    for key in sorted(ASPECT_RATIO_MAP.keys(), key=len, reverse=True):
        if key in resolution_string:
            return ASPECT_RATIO_MAP[key]
    return "1:1"

def build_prompt(prompt_data):
    negative = prompt_data.get("negative_prompt", "")
    if isinstance(negative, list):
        negative = ", ".join(negative)

    mood = prompt_data.get("mood", "")
    mood_str = f"Mood: {mood}. " if mood else ""

    authenticity = prompt_data.get("authenticity_level", "")
    auth_str = f"Authenticity level: {authenticity}. " if authenticity else ""

    motion = prompt_data["camera_settings"].get("motion_blur", "")
    motion_str = f", motion blur: {motion}" if motion and motion != "none" else ""

    return (
        f"Subject: {prompt_data['subject']['description']} {prompt_data['subject']['action']} "
        f"Setting: {prompt_data['setting']['location']} at {prompt_data['setting']['time_of_day']}. "
        f"Composition: {prompt_data['composition']['camera_angle']} {prompt_data['composition']['framing']}. "
        f"Camera: {prompt_data['camera_settings']['lens']}, {prompt_data['camera_settings']['aperture']}, "
        f"{prompt_data['camera_settings']['depth_of_field']}{motion_str}. "
        f"Lighting: {prompt_data['lighting']['type']}, {prompt_data['lighting']['color_grading']}. "
        f"{mood_str}"
        f"{auth_str}"
        f"Aesthetic: {prompt_data['aesthetic_style']}. "
        f"Format: {prompt_data['ad_format']['platform']} {prompt_data['ad_format']['ratio_and_resolution']}. "
        f"DO NOT INCLUDE: {negative}"
    )

def call_imagen_api(prompt, aspect_ratio, count, retries=2):
    headers = {
        "Content-Type": "application/json",
        "x-goog-api-key": GEMINI_API_KEY,
    }
    data = {
        "instances": [{"prompt": prompt}],
        "parameters": {
            "sampleCount": count,
            "aspectRatio": aspect_ratio,
            "outputOptions": {"mimeType": "image/png"},
        },
    }
    for attempt in range(retries + 1):
        response = requests.post(IMAGEN_URL, headers=headers, json=data)
        if response.status_code == 200:
            return response.json()
        if attempt < retries:
            print(f"  ⚠️  API error (attempt {attempt + 1}/{retries + 1}): {response.status_code} — retrying in 3s...")
            time.sleep(3)
        else:
            print(f"  ❌ API request failed: {response.status_code}")
            print(response.text)
            return None

def load_font(size, weight="bold"):
    """Load a bold font. Only bold/black weights used."""
    font_paths = [
        "/System/Library/Fonts/Supplemental/Arial Black.ttf",
        "/System/Library/Fonts/Supplemental/Impact.ttf",
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
        "/System/Library/Fonts/Helvetica.ttc",
    ]
    for fp in font_paths:
        if os.path.exists(fp):
            try:
                return ImageFont.truetype(fp, size, index=0)
            except Exception:
                try:
                    return ImageFont.truetype(fp, size)
                except Exception:
                    continue
    return ImageFont.load_default()


def wrap_text_to_lines(text, max_chars_per_line=15):
    """Break text into lines, max N chars per line. Breaks on word boundaries."""
    words = text.split()
    lines = []
    current = ""
    for word in words:
        test = f"{current} {word}".strip() if current else word
        if len(test) <= max_chars_per_line:
            current = test
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def apply_text_overlay(image_path, text_overlay):
    """Apply bold text overlay. Nike 'I'm not Nike' style only.
    No subtitles. No thin fonts. Bold headline, top-left, stacked."""
    text = text_overlay.get("text", "")
    if not text:
        return

    img = Image.open(image_path).convert("RGBA")
    w, h = img.size
    pad = int(w * 0.06)

    txt_layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(txt_layer)

    # Adapt text layout to aspect ratio
    aspect = w / h
    if aspect > 1.5:
        # Landscape: wide, shorter text
        max_chars = 20
        target_line_w = int(w * 0.50)
        base_font_pct = 0.10
    elif aspect > 0.9:
        # Square: moderate stack
        max_chars = 15
        target_line_w = int(w * 0.55)
        base_font_pct = 0.12
    else:
        # Portrait/story: tall stack OK
        max_chars = 12
        target_line_w = int(w * 0.55)
        base_font_pct = 0.08

    lines = wrap_text_to_lines(text.upper(), max_chars_per_line=max_chars)

    font_size = int(w * base_font_pct)
    font = load_font(font_size, "bold")
    widest = max(lines, key=lambda l: draw.textlength(l, font=font))
    actual_w = draw.textlength(widest, font=font)
    if actual_w > 0:
        font_size = int(font_size * target_line_w / actual_w)
        font_size = max(30, min(font_size, int(w * 0.25)))
        font = load_font(font_size, "bold")

    # Draw lines, top-left
    line_spacing = int(font_size * 1.05)
    y = pad
    for line in lines:
        draw.text((pad + 3, y + 3), line, font=font, fill=(0, 0, 0, 120))
        draw.text((pad, y), line, font=font, fill=(255, 255, 255, 255))
        y += line_spacing

    result = Image.alpha_composite(img, txt_layer).convert("RGB")
    result.save(image_path)


def image_path_for(json_path, variant=None):
    path_parts = json_path.split(os.sep)
    try:
        idx = path_parts.index("prompts")
        path_parts[idx] = "images"
    except ValueError:
        pass
    base = os.sep.join(path_parts).replace(".json", "")
    suffix = f"_v{variant}.png" if variant is not None else ".png"
    return base + suffix

def text_only(json_path):
    """Apply text overlay to existing images without regenerating."""
    if not os.path.exists(json_path):
        print(f"  ❌ File not found: {json_path}")
        return []

    with open(json_path, "r") as f:
        prompt_data = json.load(f)

    text_overlay = prompt_data.get("text_overlay", {})
    if not text_overlay or not text_overlay.get("text"):
        print(f"  ⚠️  No text_overlay in {json_path}")
        return []

    # Find existing images for this prompt
    base_path = image_path_for(json_path)
    img_dir = os.path.dirname(base_path)
    base_name = os.path.basename(base_path).replace(".png", "")

    matched = []
    if os.path.isdir(img_dir):
        for f in os.listdir(img_dir):
            if f.startswith(base_name) and f.endswith(".png"):
                matched.append(os.path.join(img_dir, f))

    if not matched:
        print(f"  ❌ No existing images found for {json_path}")
        return []

    print(f"\n🔤 Applying text overlay to {len(matched)} image(s)...")
    for img_path in sorted(matched):
        apply_text_overlay(img_path, text_overlay)
        print(f"  ✅ Text applied: {img_path}")

    return matched


def resize_image(source_path, json_path, bias=0.5):
    """Resize approved image to target dimensions from JSON prompt.
    Uses 'cover' fit: scales to fill, then crops to exact size.
    bias: 0.0=crop from top, 0.5=center crop, 1.0=crop from bottom."""
    import re

    if not os.path.exists(source_path):
        print(f"  ❌ Source image not found: {source_path}")
        return None
    if not os.path.exists(json_path):
        print(f"  ❌ JSON not found: {json_path}")
        return None

    with open(json_path, "r") as f:
        prompt_data = json.load(f)

    resolution = prompt_data["ad_format"]["ratio_and_resolution"]
    match = re.search(r'(\d+)x(\d+)', resolution)
    if not match:
        print(f"  ❌ Can't parse resolution from: {resolution}")
        return None

    target_w, target_h = int(match.group(1)), int(match.group(2))

    img = Image.open(source_path).convert("RGB")
    src_w, src_h = img.size

    # Cover fit: scale to fill target ratio, then center-crop
    src_ratio = src_w / src_h
    target_ratio = target_w / target_h

    if src_ratio > target_ratio:
        # Source is wider than target — crop left/right (bias on horizontal)
        new_w = int(src_h * target_ratio)
        max_left = src_w - new_w
        left = int(max_left * bias)
        img = img.crop((left, 0, left + new_w, src_h))
    elif src_ratio < target_ratio:
        # Source is taller than target — crop top/bottom (bias on vertical)
        new_h = int(src_w / target_ratio)
        max_top = src_h - new_h
        top = int(max_top * bias)
        img = img.crop((0, top, src_w, top + new_h))

    # Resize to exact target dimensions
    img = img.resize((target_w, target_h), Image.LANCZOS)

    out_path = image_path_for(json_path)
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    img.save(out_path, quality=95)

    # Apply text overlay if present
    text_overlay = prompt_data.get("text_overlay", {})
    if text_overlay and text_overlay.get("text"):
        apply_text_overlay(out_path, text_overlay)
        print(f"  ✅ Resized + text: {out_path}")
    else:
        print(f"  ✅ Resized: {out_path}")

    return out_path


def generate(json_path, count=1, auto_open=False):
    if not os.path.exists(json_path):
        print(f"  ❌ File not found: {json_path}")
        return []

    with open(json_path, "r") as f:
        prompt_data = json.load(f)

    full_prompt = build_prompt(prompt_data)
    aspect_ratio = get_aspect_ratio(prompt_data["ad_format"]["ratio_and_resolution"])

    print(f"\n🔄 Generating {count} image(s) from {json_path} [{aspect_ratio}]...")

    resp = call_imagen_api(full_prompt, aspect_ratio, count)
    if not resp:
        return []

    predictions = resp.get("predictions", [])
    if not predictions:
        print("  ❌ API returned no predictions:", resp)
        return []

    text_overlay = prompt_data.get("text_overlay", {})

    saved_paths = []
    for i, pred in enumerate(predictions):
        variant = (i + 1) if count > 1 else None
        out_path = image_path_for(json_path, variant)
        os.makedirs(os.path.dirname(out_path), exist_ok=True)
        image_bytes = base64.b64decode(pred["bytesBase64Encoded"])
        with open(out_path, "wb") as img_file:
            img_file.write(image_bytes)
        if text_overlay and text_overlay.get("text"):
            apply_text_overlay(out_path, text_overlay)
            print(f"  ✅ Saved + text: {out_path}")
        else:
            print(f"  ✅ Saved: {out_path}")
        saved_paths.append(out_path)
        if auto_open:
            subprocess.run(["open", out_path], check=False)

    return saved_paths

def main():
    parser = argparse.ArgumentParser(
        description="Generate ad images from JSON prompt files using Imagen 4.0."
    )
    parser.add_argument(
        "path",
        help="Path to a single JSON prompt file, or a directory to batch-generate all .json files in it.",
    )
    parser.add_argument(
        "--count",
        type=int,
        default=1,
        metavar="N",
        help="Number of image variants to generate per prompt (default: 1). Saved as _v1.png, _v2.png, etc.",
    )
    parser.add_argument(
        "--open",
        action="store_true",
        dest="auto_open",
        help="Automatically open each generated image in the system viewer after saving.",
    )
    parser.add_argument(
        "--text-only",
        action="store_true",
        dest="text_only",
        help="Apply text overlay to existing images without regenerating. Reads text_overlay from the JSON prompt and applies it to the corresponding image files.",
    )
    parser.add_argument(
        "--resize",
        metavar="SOURCE",
        help="Resize an approved source image to the dimensions specified in the JSON prompt. No API call — just crop and resize.",
    )
    parser.add_argument(
        "--bias",
        type=float,
        default=0.5,
        help="Crop bias (0.0=top, 0.5=center, 1.0=bottom). Used with --resize. Default: 0.5",
    )
    args = parser.parse_args()

    path = args.path

    if args.resize:
        # Resize mode: crop/resize approved image to target size from JSON
        if os.path.isfile(path):
            result = resize_image(args.resize, path, bias=args.bias)
            if result:
                print(f"\n🎉 Done. Resized to {result}")
            else:
                print("\n❌ Resize failed.")
                sys.exit(1)
        elif os.path.isdir(path):
            json_files = sorted(glob.glob(os.path.join(path, "*.json")))
            if not json_files:
                print(f"No .json files found in {path}")
                sys.exit(1)
            print(f"\n📐 Resizing approved image to {len(json_files)} size(s)...")
            for jf in json_files:
                resize_image(args.resize, jf, bias=args.bias)
            print(f"\n🎉 Done. {len(json_files)} size(s) created.")
        else:
            print(f"Error: '{path}' is not a valid file or directory.")
            sys.exit(1)
    elif args.text_only:
        # Text-only mode: apply text overlay to existing images
        if os.path.isdir(path):
            json_files = sorted(glob.glob(os.path.join(path, "*.json")))
            if not json_files:
                print(f"No .json files found in {path}")
                sys.exit(1)
            all_processed = []
            for jf in json_files:
                processed = text_only(jf)
                all_processed.extend(processed)
            print(f"\n🎉 Done. Text applied to {len(all_processed)} image(s).")
        elif os.path.isfile(path):
            processed = text_only(path)
            print(f"\n🎉 Done. Text applied to {len(processed)} image(s).")
        else:
            print(f"Error: '{path}' is not a valid file or directory.")
            sys.exit(1)
    elif os.path.isdir(path):
        json_files = sorted(glob.glob(os.path.join(path, "*.json")))
        if not json_files:
            print(f"No .json files found in {path}")
            sys.exit(1)
        print(f"📂 Batch mode: {len(json_files)} prompt(s) found in {path}")
        all_saved = []
        for jf in json_files:
            saved = generate(jf, count=args.count, auto_open=args.auto_open)
            all_saved.extend(saved)
        print(f"\n🎉 Done. {len(all_saved)} image(s) generated.")
    elif os.path.isfile(path):
        saved = generate(path, count=args.count, auto_open=args.auto_open)
        print(f"\n🎉 Done. {len(saved)} image(s) generated.")
    else:
        print(f"Error: '{path}' is not a valid file or directory.")
        sys.exit(1)

if __name__ == "__main__":
    main()
