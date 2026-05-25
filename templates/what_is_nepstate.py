"""
Template: WHAT IS NEPSTATE
Friday video — who we are, what we do, community platform intro.
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from PIL import Image, ImageDraw
from common import *
import math

OUTPUT = "marketing-video.mp4"

SECTIONS = [
    {
        "title": "What is NepState?",
        "body": "A FREE community platform\nbuilt for Nepalis living in the US",
        "color": COLOR_RED,
        "emoji": "🇳🇵"
    },
    {
        "title": "Find What You Need",
        "body": "Events • Jobs • Housing\nNepali Businesses • Community Blog",
        "color": COLOR_GOLD,
        "emoji": "🔍"
    },
    {
        "title": "Share With Your Community",
        "body": "Post events, job openings,\nrooms for rent — all for FREE",
        "color": COLOR_GREEN,
        "emoji": "📢"
    },
    {
        "title": "Trusted & Verified",
        "body": "117+ Nepali businesses listed\nReviews, photos & contact info",
        "color": (37, 99, 235),
        "emoji": "✅"
    },
]

def generate_frame(i, total):
    progress = i / total
    img = Image.new('RGB', (VIDEO_WIDTH, VIDEO_HEIGHT), COLOR_BG_TOP)
    draw_gradient_bg(img)
    draw = ImageDraw.Draw(img)

    draw_header(draw, progress)

    # Animated subtitle
    t_sub = ease_out(min(1.0, (progress - 0.1) * 4))
    sub_y = int(lerp(-50, 0, t_sub))
    draw.text((540, 250+sub_y), "Your Nepali Community Hub in the US",
              font=get_font(38, bold=True), fill=COLOR_GOLD_LIGHT, anchor="mm")

    # Decorative divider
    t_div = ease_out(min(1.0, (progress - 0.15) * 5))
    div_w = int(lerp(0, 400, t_div))
    draw.rectangle([540-div_w//2, 295, 540+div_w//2, 299], fill=COLOR_RED)

    # Section cards
    card_top = 330
    card_h   = 310
    card_gap = 18
    pad      = 50

    for idx, sec in enumerate(SECTIONS):
        delay = 0.06 * idx
        t = ease_out(min(1.0, max(0.0, (progress - 0.18 - delay) * 3.5)))
        alpha_off = int(lerp(80, 0, t))   # slide from right for even, left for odd
        slide = int(lerp(VIDEO_WIDTH + 60 if idx % 2 == 0 else -VIDEO_WIDTH - 60, 0, t))

        top = card_top + idx * (card_h + card_gap)
        bot = top + card_h
        draw_rounded_rect(draw, [pad+slide, top, VIDEO_WIDTH-pad+slide, bot],
                          24, COLOR_CARD_DARK, outline=sec["color"], outline_width=3)

        # Large emoji left
        draw.text((pad + 90 + slide, top + card_h//2 - 20), sec["emoji"],
                  font=get_font(74), anchor="mm")

        # Colored accent bar
        draw.rectangle([pad + 155 + slide, top + 30, pad + 161 + slide, bot - 30],
                       fill=sec["color"])

        # Text
        draw.text((pad + 180 + slide, top + 75), sec["title"],
                  font=get_font(44, bold=True), fill=sec["color"], anchor="lm")
        for li, line in enumerate(sec["body"].split("\n")):
            draw.text((pad + 180 + slide, top + 140 + li * 48), line,
                      font=get_font(32), fill=COLOR_WHITE, anchor="lm")

    # Stats bar at bottom
    t_stats = ease_out(max(0.0, (progress - 0.55) * 3))
    sy = int(lerp(100, 0, t_stats))
    stats_top = 1680
    draw_rounded_rect(draw, [40, stats_top+sy, 1040, 1710+sy], 16,
                      (40, 20, 20), outline=COLOR_GOLD, outline_width=2)
    stats = [("28+", "Cities"), ("117+", "Businesses"), ("FREE", "Always")]
    for si, (num, label) in enumerate(stats):
        x = 190 + si * 300
        draw.text((x, stats_top + 22 + sy), num,
                  font=get_font(40, bold=True), fill=COLOR_GOLD_LIGHT, anchor="mm")
        draw.text((x, stats_top + 62 + sy), label,
                  font=get_font(26), fill=COLOR_MUTED, anchor="mm")

    draw_cta(draw, progress, cta_text="Join the community →")
    return img

def get_caption():
    return """\
🇳🇵 What is NepState? Your Nepali Community Hub in the US!

🔍 Find Nepali events, jobs, housing & businesses near you
📢 Post for FREE — events, job openings, rooms for rent
✅ 117+ verified Nepali businesses listed
🌎 Available in 28+ US cities

Built by Nepalis, for Nepalis.
100% FREE — always.

👉 nepstate.com

#NepState #WhatIsNepState #NepaliUSA #NepaliCommunity
#NepaliAmerica #NepalDiaspora #ConnectingNepaleseGlobally"""

def run():
    print("🎬 Generating: What Is NepState")
    os.makedirs(FRAMES_DIR, exist_ok=True)
    total = FPS * DURATION
    for i in range(total):
        generate_frame(i, total).save(f"{FRAMES_DIR}/frame_{i:04d}.png")
        if i % 60 == 0: print(f"   {i}/{total} frames...")
    return compile_video(OUTPUT), get_caption()

if __name__ == "__main__":
    run()
