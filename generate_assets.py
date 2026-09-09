"""
Generates lightweight animated GIFs of an elegant tall girl (Miss India / runway model style):
- walk_left.gif (Graceful runway walk left)
- drink.gif (Gracefully holding an elegant glass of water and sipping)
- walk_right.gif (Graceful runway walk right)

All frames have 100% transparent background with NO circles or background shapes.
"""
import math
from PIL import Image, ImageDraw

def draw_tall_model_frame(frame_idx, total_frames, action="walk", direction="left"):
    # Tall 160 x 300 canvas for elegant model proportions
    width, height = 160, 300
    img = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Walk cycle math
    phase = 2 * math.pi * (frame_idx / total_frames)
    bounce = int(3 * math.sin(phase))
    hip_sway = int(3 * math.sin(phase))
    
    # Direction offset
    dx = -4 if direction == "left" else (4 if direction == "right" else 0)
    center_x = 80 + dx

    # Colors
    skin_tone = (243, 204, 175, 255)
    skin_shadow = (220, 175, 140, 255)
    hair_color = (25, 20, 25, 255)
    hair_shine = (80, 65, 75, 255)
    gown_color = (147, 51, 234, 255)       # Royal Indian purple / violet gown
    gown_highlight = (192, 132, 252, 255)
    gown_shadow = (107, 33, 168, 255)
    gold_sash = (245, 158, 11, 255)        # Miss India golden pageant sash
    gold_highlight = (252, 211, 77, 255)
    tiara_color = (250, 204, 21, 255)
    lip_color = (225, 29, 72, 255)
    blush_color = (251, 113, 133, 150)

    # ---------------- 1. Long Flowing Hair (Back Layer) ----------------
    hair_sway = int(4 * math.sin(phase)) if action == "walk" else 0
    # Long flowing glossy black hair down past waist
    draw.polygon([
        (center_x - 18, 55 + bounce),
        (center_x + 18, 55 + bounce),
        (center_x + 28 + hair_sway, 145 + bounce),
        (center_x - 28 + hair_sway, 145 + bounce)
    ], fill=hair_color)

    # ---------------- 2. Legs & High Heels ----------------
    if action == "walk":
        leg_phase = math.sin(phase)
        foot_l_y = int(12 * leg_phase)
        foot_r_y = int(-12 * leg_phase)
        foot_l_x = int(6 * leg_phase)
        foot_r_x = int(-6 * leg_phase)

        # Left Leg (Tall & slender)
        draw.line([(center_x - 8 + hip_sway, 165 + bounce), (center_x - 10 + foot_l_x, 235), (center_x - 10 + foot_l_x, 275 - foot_l_y)], fill=skin_tone, width=9)
        # Left Golden Heel
        draw.polygon([
            (center_x - 14 + foot_l_x, 275 - foot_l_y),
            (center_x - 4 + foot_l_x, 275 - foot_l_y),
            (center_x - 6 + foot_l_x, 285 - foot_l_y),
            (center_x - 12 + foot_l_x, 285 - foot_l_y)
        ], fill=gold_sash)
        # Heel spike
        draw.line([(center_x - 12 + foot_l_x, 280 - foot_l_y), (center_x - 12 + foot_l_x, 290 - foot_l_y)], fill=gold_sash, width=2)

        # Right Leg
        draw.line([(center_x + 8 + hip_sway, 165 + bounce), (center_x + 10 + foot_r_x, 235), (center_x + 10 + foot_r_x, 275 - foot_r_y)], fill=skin_tone, width=9)
        # Right Golden Heel
        draw.polygon([
            (center_x + 6 + foot_r_x, 275 - foot_r_y),
            (center_x + 16 + foot_r_x, 275 - foot_r_y),
            (center_x + 14 + foot_r_x, 285 - foot_r_y),
            (center_x + 8 + foot_r_x, 285 - foot_r_y)
        ], fill=gold_sash)
        draw.line([(center_x + 8 + foot_r_x, 280 - foot_r_y), (center_x + 8 + foot_r_x, 290 - foot_r_y)], fill=gold_sash, width=2)
    else:
        # Elegant Standing Pose
        draw.line([(center_x - 7, 165 + bounce), (center_x - 6, 235), (center_x - 8, 278)], fill=skin_tone, width=9)
        draw.line([(center_x + 7, 165 + bounce), (center_x + 9, 235), (center_x + 11, 278)], fill=skin_tone, width=9)
        # Heels
        draw.polygon([(center_x - 12, 278), (center_x - 2, 278), (center_x - 4, 287), (center_x - 10, 287)], fill=gold_sash)
        draw.line([(center_x - 10, 282), (center_x - 10, 292)], fill=gold_sash, width=2)
        draw.polygon([(center_x + 6, 278), (center_x + 16, 278), (center_x + 14, 287), (center_x + 8, 287)], fill=gold_sash)
        draw.line([(center_x + 8, 282), (center_x + 8, 292)], fill=gold_sash, width=2)

    # ---------------- 3. Elegant Slit Gown & Waist ----------------
    # Flowing slit gown
    slit_offset = 6 if direction == "left" else -6
    draw.polygon([
        (center_x - 16 + hip_sway, 115 + bounce),
        (center_x + 16 + hip_sway, 115 + bounce),
        (center_x + 24 + hip_sway, 210 + bounce),
        (center_x - 24 + hip_sway, 210 + bounce)
    ], fill=gown_color, outline=gown_shadow)

    # Gown folds/highlights
    draw.line([(center_x - 6 + hip_sway, 120 + bounce), (center_x - 12 + hip_sway, 205 + bounce)], fill=gown_highlight, width=2)
    draw.line([(center_x + 6 + hip_sway, 120 + bounce), (center_x + 12 + hip_sway, 205 + bounce)], fill=gown_highlight, width=2)

    # Gown Bodice (Fitted Top)
    draw.polygon([
        (center_x - 14 + hip_sway, 78 + bounce),
        (center_x + 14 + hip_sway, 78 + bounce),
        (center_x + 16 + hip_sway, 115 + bounce),
        (center_x - 16 + hip_sway, 115 + bounce)
    ], fill=gown_color)

    # ---------------- 4. Miss India Golden Sash ----------------
    draw.polygon([
        (center_x - 12 + hip_sway, 80 + bounce),
        (center_x - 6 + hip_sway, 78 + bounce),
        (center_x + 16 + hip_sway, 130 + bounce),
        (center_x + 10 + hip_sway, 134 + bounce)
    ], fill=gold_sash, outline=gold_highlight)

    # ---------------- 5. Neck, Chest & Collarbone ----------------
    draw.rectangle([center_x - 5, 62 + bounce, center_x + 5, 76 + bounce], fill=skin_tone)
    draw.arc([center_x - 8, 70 + bounce, center_x + 8, 76 + bounce], start=0, end=180, fill=skin_shadow, width=1)

    # ---------------- 6. Arms & Actions ----------------
    if action == "walk":
        arm_swing = int(8 * math.sin(phase))
        # Runway posture arms swinging gracefully
        draw.line([(center_x - 14, 82 + bounce), (center_x - 20 - arm_swing, 112 + bounce), (center_x - 24 - arm_swing, 140 + bounce)], fill=skin_tone, width=5)
        draw.line([(center_x + 14, 82 + bounce), (center_x + 20 + arm_swing, 112 + bounce), (center_x + 24 + arm_swing, 140 + bounce)], fill=skin_tone, width=5)
        # Golden bangles
        draw.ellipse([center_x - 26 - arm_swing, 132 + bounce, center_x - 22 - arm_swing, 138 + bounce], fill=gold_sash)
        draw.ellipse([center_x + 22 + arm_swing, 132 + bounce, center_x + 26 + arm_swing, 138 + bounce], fill=gold_sash)
    else:
        # Action: Gracefully holding an elegant sparkling glass of water to drink
        # Left arm resting gracefully on waist
        draw.line([(center_x - 14, 82 + bounce), (center_x - 24, 105 + bounce), (center_x - 14, 115 + bounce)], fill=skin_tone, width=5)
        # Right arm bent holding water glass near mouth
        draw.line([(center_x + 14, 82 + bounce), (center_x + 26, 95 + bounce), (center_x + 8, 58 + bounce)], fill=skin_tone, width=5)
        
        # Elegant crystal water glass
        draw.polygon([
            (center_x + 6, 48 + bounce),
            (center_x + 20, 48 + bounce),
            (center_x + 17, 68 + bounce),
            (center_x + 9, 68 + bounce)
        ], fill=(255, 255, 255, 220), outline=(56, 189, 248, 255))
        # Pure blue water inside
        draw.polygon([
            (center_x + 8, 54 + bounce),
            (center_x + 18, 54 + bounce),
            (center_x + 16, 66 + bounce),
            (center_x + 10, 66 + bounce)
        ], fill=(14, 165, 233, 230))
        # Water sparkle ✨
        draw.line([(center_x + 13, 44 + bounce), (center_x + 13, 46 + bounce)], fill=(255, 255, 255, 255), width=2)
        draw.line([(center_x + 12, 45 + bounce), (center_x + 14, 45 + bounce)], fill=(255, 255, 255, 255), width=2)

    # ---------------- 7. Elegant Face & Miss India Crown/Tiara ----------------
    # Slender graceful face
    draw.polygon([
        (center_x - 11, 40 + bounce),
        (center_x + 11, 40 + bounce),
        (center_x + 7, 62 + bounce),
        (center_x, 66 + bounce),
        (center_x - 7, 62 + bounce)
    ], fill=skin_tone)

    # Elegant almond-shaped eyes with eyeliner & eyelashes
    if action == "walk":
        # Almond eye left
        draw.ellipse([center_x - 9, 47 + bounce, center_x - 3, 53 + bounce], fill=(20, 20, 25, 255))
        draw.ellipse([center_x - 7, 48 + bounce, center_x - 5, 51 + bounce], fill=(255, 255, 255, 255))
        # Eyeliner flick left
        draw.line([(center_x - 9, 47 + bounce), (center_x - 12, 45 + bounce)], fill=(10, 10, 15, 255), width=2)

        # Almond eye right
        draw.ellipse([center_x + 3, 47 + bounce, center_x + 9, 53 + bounce], fill=(20, 20, 25, 255))
        draw.ellipse([center_x + 5, 48 + bounce, center_x + 7, 51 + bounce], fill=(255, 255, 255, 255))
        # Eyeliner flick right
        draw.line([(center_x + 9, 47 + bounce), (center_x + 12, 45 + bounce)], fill=(10, 10, 15, 255), width=2)

        # Cheeks blush
        draw.ellipse([center_x - 10, 53 + bounce, center_x - 4, 57 + bounce], fill=blush_color)
        draw.ellipse([center_x + 4, 53 + bounce, center_x + 10, 57 + bounce], fill=blush_color)
        # Elegant Red Lips
        draw.ellipse([center_x - 4, 58 + bounce, center_x + 4, 62 + bounce], fill=lip_color)
    else:
        # Happy model smile while sipping
        draw.arc([center_x - 9, 46 + bounce, center_x - 3, 52 + bounce], start=180, end=360, fill=(20, 20, 25, 255), width=2)
        draw.arc([center_x + 3, 46 + bounce, center_x + 9, 52 + bounce], start=180, end=360, fill=(20, 20, 25, 255), width=2)
        draw.ellipse([center_x - 10, 53 + bounce, center_x - 4, 57 + bounce], fill=blush_color)
        draw.ellipse([center_x + 4, 53 + bounce, center_x + 10, 57 + bounce], fill=blush_color)
        draw.ellipse([center_x - 4, 58 + bounce, center_x + 4, 63 + bounce], fill=lip_color)

    # Hair framing face & forehead
    draw.polygon([(center_x - 12, 38 + bounce), (center_x, 34 + bounce), (center_x + 12, 38 + bounce), (center_x + 12, 46 + bounce), (center_x - 12, 46 + bounce)], fill=hair_color)

    # ---------------- 8. Miss India Sparkling Tiara / Crown ----------------
    draw.polygon([
        (center_x - 10, 36 + bounce),
        (center_x - 7, 24 + bounce),
        (center_x - 3, 30 + bounce),
        (center_x, 20 + bounce),       # Tall center peak
        (center_x + 3, 30 + bounce),
        (center_x + 7, 24 + bounce),
        (center_x + 10, 36 + bounce)
    ], fill=tiara_color, outline=(254, 240, 138, 255))
    # Diamond jewels on tiara
    draw.ellipse([center_x - 1, 23 + bounce, center_x + 1, 25 + bounce], fill=(255, 255, 255, 255))
    draw.ellipse([center_x - 8, 27 + bounce, center_x - 6, 29 + bounce], fill=(255, 255, 255, 255))
    draw.ellipse([center_x + 6, 27 + bounce, center_x + 8, 29 + bounce], fill=(255, 255, 255, 255))

    return img

def generate_gif(filename, action, direction, frames=8, duration=120):
    images = []
    for i in range(frames):
        images.append(draw_tall_model_frame(i, frames, action, direction))
    
    images[0].save(
        filename,
        save_all=True,
        append_images=images[1:],
        duration=duration,
        loop=0,
        disposal=2
    )
    print(f"Generated {filename}")

if __name__ == "__main__":
    generate_gif("walk_left.gif", action="walk", direction="left")
    generate_gif("drink.gif", action="drink", direction="none")
    generate_gif("walk_right.gif", action="walk", direction="right")
