"""
Template: POST FOR FREE
Monday video — promotes free posting of Events, Jobs, Housing, Directory.
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from PIL import Image, ImageDraw
from common import *
import math

OUTPUT = "marketing-video.mp4"

CARDS = [
    {"emoji": "🎉", "title": "Events",   "sub": "Dashain parties, concerts,\ncultural shows & more",   "color": COLOR_RED},
    {"emoji": "💼", "title": "Jobs",     "sub": "Nepali-friendly job listings\nacross the US",           "color": (37, 99, 235)},
    {"emoji": "🏠", "title": "Housing",  "sub": "Rooms & apartments with\nNepali roommates",            "color": COLOR_GREEN},
    {"emoji": "🗺️", "title": "Directory","sub": "Find trusted Nepali businesses\nnear you",             "color": (126, 34, 206)},
]

def generate_frame(i, total):
    progress = i / total
    img = Image.new('RGB', (VIDEO_WIDTH, VIDEO_HEIGHT), COLOR_BG_TOP)
    draw_gradient_bg(img)
    draw = ImageDraw.Draw(img)

    draw_header(draw, progress, "Post for FREE — Takes 2 minutes!")

    # Hero line
    t_hero = ease_out(min(1.0, (progress - 0.1) * 4))
    hero_y = int(lerp(-80, 0, t_hero))
    draw.text((540, 260+hero_y), "🇳🇵 Nepalis in the US —",
              font=get_nepali_font(44, bold=True), fill=COLOR_GOLD_LIGHT, anchor="mm")
    draw.text((540, 320+hero_y), "NepState is YOUR platform",
              font=get_font(42, bold=True), fill=COLOR_WHITE, anchor="mm")

    # 4 category cards
    card_top = 390
    card_h   = 295
    card_gap = 20
    pad      = 50

    for idx, card in enumerate(CARDS):
        delay = 0.05 * idx
        t = ease_out(min(1.0, max(0.0, (progress - 0.15 - delay) * 4)))
        slide = int(lerp(VIDEO_WIDTH + 100, 0, t))

        top = card_top + idx * (card_h + card_gap)
        bot = top + card_h
        draw_rounded_rect(draw, [pad+slide, top, VIDEO_WIDTH-pad+slide, bot],
                          22, COLOR_CARD_DARK, outline=card["color"], outline_width=3)

        # Emoji
        draw.text((pad + 80 + slide, top + card_h//2), card["emoji"],
                  font=get_font(68), anchor="mm")

        # Title
        draw.text((pad + 170 + slide, top + 80), card["title"],
                  font=get_font(56, bold=True), fill=COLOR_WHITE, anchor="lm")

        # Subtitle (multi-line)
        for li, line in enumerate(card["sub"].split("\n")):
            draw.text((pad + 170 + slide, top + 145 + li * 40), line,
                      font=get_font(30), fill=COLOR_MUTED, anchor="lm")

        # FREE badge
        draw_rounded_rect(draw,
            [VIDEO_WIDTH - pad - 120 + slide, top + card_h//2 - 28,
             VIDEO_WIDTH - pad - 10  + slide, top + card_h//2 + 28],
            14, card["color"])
        draw.text((VIDEO_WIDTH - pad - 65 + slide, top + card_h//2),
                  "FREE", font=get_font(26, bold=True), fill=COLOR_WHITE, anchor="mm")

    draw_cta(draw, progress, cta_text="Start posting now →")
    return img

def get_caption():
    return """\
🇳🇵 NepState — Your Free Nepali Community Platform!

✅ Post Events (festivals, concerts, cultural shows)
✅ Post Jobs (find or hire Nepali talent)
✅ Post Housing (rooms, apartments, roommates)
✅ Find Nepali Businesses near you

100% FREE • Takes less than 2 minutes!
👉 nepstate.com/post-listing

#NepState #NepaliUSA #NepaliCommunity #NepaliEvents #NepaliJobs
#NepaliHousing #NepalDiaspora #ConnectingNepaleseGlobally"""

def run():
    print("🎬 Generating: Post For Free")
    os.makedirs(FRAMES_DIR, exist_ok=True)
    total = FPS * DURATION
    for i in range(total):
        generate_frame(i, total).save(f"{FRAMES_DIR}/frame_{i:04d}.png")
        if i % 60 == 0: print(f"   {i}/{total} frames...")
    return compile_video(OUTPUT), get_caption()

if __name__ == "__main__":
    run()
