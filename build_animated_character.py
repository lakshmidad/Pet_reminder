"""
Generates the animated character GIFs for Pet Reminder with exact directions:
- walk_left.gif : Girl turned LEFT and walking LEFT (Entrance)
- drink.gif     : Girl in drinking posture sipping water (In place)
- walk_right.gif: Girl turned RIGHT and walking RIGHT (Exit)

All frames have 100% transparent background with NO ground circles or shadows.
"""
import math
import os
from PIL import Image, ImageDraw, ImageOps
import numpy as np


def clean_character_image(img_path, remove_bottom_shadow=True):
    """Extract character onto 100% transparent background and remove ground shadow."""
    img = Image.open(img_path).convert("RGBA")
    arr = np.array(img)
    h, w = arr.shape[:2]

    # Background floodfill from (0,0)
    bg_color = arr[0, 0, :3]
    dist = np.sqrt(np.sum((arr[:, :, :3].astype(float) - bg_color.astype(float)) ** 2, axis=2))
    is_bg = dist < 32

    mask = Image.fromarray((is_bg * 255).astype(np.uint8))
    padded = ImageOps.expand(mask, border=1, fill=255)
    ImageDraw.floodfill(padded, (0, 0), value=128)
    filled = np.array(padded.crop((1, 1, w + 1, h + 1)))
    arr[filled == 128, 3] = 0

    # Remove oval ground shadow beneath feet if requested
    if remove_bottom_shadow:
        bottom_start = int(h * 0.80)
        r, g, b, a = arr[:, :, 0], arr[:, :, 1], arr[:, :, 2], arr[:, :, 3]
        is_shadow = np.zeros((h, w), dtype=bool)
        is_shadow[bottom_start:, :] = (
            (a[bottom_start:, :] > 0)
            & (r[bottom_start:, :] > 195)
            & (g[bottom_start:, :] > 175)
            & (b[bottom_start:, :] > 160)
            & ((r[bottom_start:, :].astype(int) - b[bottom_start:, :].astype(int)) < 55)
            & ~((r[bottom_start:, :] > 250) & (g[bottom_start:, :] > 250) & (b[bottom_start:, :] > 250))
        )
        arr[is_shadow, 3] = 0

    out = Image.fromarray(arr)
    bbox = out.getbbox()
    if bbox:
        margin = 4
        out = out.crop(
            (
                max(0, bbox[0] - margin),
                max(0, bbox[1] - margin),
                min(w, bbox[2] + margin),
                min(h, bbox[3] + margin),
            )
        )
    return out


def create_animated_drink_gif(drink_img, out_path, num_frames=10, target_size=(240, 280)):
    """Create drinking animation with cute breathing, glass sipping motion, and water sparkles."""
    aspect = drink_img.width / drink_img.height
    new_h = int(target_size[1] * 0.90)
    new_w = int(new_h * aspect)
    base = drink_img.resize((new_w, new_h), Image.Resampling.LANCZOS)

    frames = []
    for i in range(num_frames):
        canvas = Image.new("RGBA", target_size, (0, 0, 0, 0))

        phase = 2 * math.pi * (i / num_frames)
        bounce = int(3 * math.sin(phase))

        pos_x = (target_size[0] - new_w) // 2
        pos_y = target_size[1] - new_h - 10 + bounce

        canvas.paste(base, (pos_x, pos_y), base)

        # Sparkle effect on water glass
        draw = ImageDraw.Draw(canvas)
        sparkle_idx = i % 5
        if sparkle_idx in (1, 2, 3):
            sp_x = pos_x + int(new_w * 0.78)
            sp_y = pos_y + int(new_h * 0.38) - (sparkle_idx * 2)
            draw.line([(sp_x - 3, sp_y), (sp_x + 3, sp_y)], fill=(56, 189, 248, 240), width=2)
            draw.line([(sp_x, sp_y - 3), (sp_x, sp_y + 3)], fill=(56, 189, 248, 240), width=2)
            draw.ellipse([sp_x - 1, sp_y - 1, sp_x + 1, sp_y + 1], fill=(255, 255, 255, 255))

        frames.append(canvas)

    frames[0].save(
        out_path,
        save_all=True,
        append_images=frames[1:],
        duration=120,
        loop=0,
        disposal=2,
    )
    print(f"Generated {out_path} successfully.")


def create_animated_walk_cycle(base_img, out_path, direction="left", num_frames=10, target_size=(240, 280)):
    """
    Creates a walking animation where:
    - direction == 'left' : Girl turns LEFT and walks towards LEFT (FLIP_LEFT_RIGHT)
    - direction == 'right': Girl turns RIGHT and walks towards RIGHT (Original facing right)
    """
    # Source image faces RIGHT.
    # If walking LEFT: flip so girl turns and faces LEFT.
    # If walking RIGHT: keep as is so girl turns and faces RIGHT.
    if direction == "left":
        walk_img = base_img.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
    else:
        walk_img = base_img.copy()

    aspect = walk_img.width / walk_img.height
    new_h = int(target_size[1] * 0.90)
    new_w = int(new_h * aspect)
    base = walk_img.resize((new_w, new_h), Image.Resampling.LANCZOS)

    frames = []
    for i in range(num_frames):
        canvas = Image.new("RGBA", target_size, (0, 0, 0, 0))

        phase = 2 * math.pi * (i / num_frames)
        bounce = int(6 * math.sin(phase * 2))  # Double vertical bounce per stride cycle
        stride_sway = int(4 * math.sin(phase))  # Horizontal stride sway

        pos_x = (target_size[0] - new_w) // 2 + stride_sway
        pos_y = target_size[1] - new_h - 10 + abs(bounce)

        # Slight tilt for walking motion
        angle = 1.5 * math.sin(phase)
        rotated = base.rotate(angle, resample=Image.Resampling.BICUBIC, expand=True)
        r_w, r_h = rotated.size
        offset_x = pos_x - (r_w - new_w) // 2
        offset_y = pos_y - (r_h - new_h) // 2

        canvas.paste(rotated, (offset_x, offset_y), rotated)
        frames.append(canvas)

    frames[0].save(
        out_path,
        save_all=True,
        append_images=frames[1:],
        duration=100,
        loop=0,
        disposal=2,
    )
    print(f"Generated {out_path} (Facing {direction.upper()}).")


if __name__ == "__main__":
    drink_source = r"C:\Users\mindy\.gemini\antigravity-ide\brain\a787af20-67f3-46b3-89af-4eddd27d9c32\.user_uploaded\media_1788853986249.png"
    walk_source = r"C:\Users\mindy\.gemini\antigravity-ide\brain\a787af20-67f3-46b3-89af-4eddd27d9c32\girl_walking_pose_1788854060182.jpg"

    clean_drink = clean_character_image(drink_source, remove_bottom_shadow=False)
    clean_walk = clean_character_image(walk_source, remove_bottom_shadow=True)

    # 1. Generate drink animation (In-place drinking posture)
    create_animated_drink_gif(clean_drink, "drink.gif")

    # 2. Generate walk_left.gif (Girl turned LEFT and walking LEFT)
    create_animated_walk_cycle(clean_walk, "walk_left.gif", direction="left")

    # 3. Generate walk_right.gif (Girl turned RIGHT and walking RIGHT)
    create_animated_walk_cycle(clean_walk, "walk_right.gif", direction="right")

    print("All GIFs updated and regenerated successfully!")
