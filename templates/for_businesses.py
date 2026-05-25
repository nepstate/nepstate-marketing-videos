"""
Template: FOR BUSINESSES
Wednesday video — how NepState helps Nepali businesses get discovered.
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from PIL import Image, ImageDraw
from common import *
import math

OUTPUT = "marketing-video.mp4"

BENEFITS = [
    ("📍", "Free Business Listing",   "Get discovered by thousands\nof Nepalis in the US"),
    ("⭐", "Reviews & Ratings",        "Build trust with verified\ncustomer reviews"),
    ("📞", "Direct Contact",           "Phone, WhatsApp & email\nright on your profile"),
    ("🕐", "Business Hours",           "Show when you're open\nso customers can plan"),
    ("📸", "Photo Gallery",            "Showcase your business\nwith beautiful photos"),
    ("🏆", "Spotlight Listings",       "Get featured at the top\nfor maximum visibility"),
]

def generate_frame(i, total):
    progress = i / total
    img = Image.new('RGB', (VIDEO_WIDTH, VIDEO_HEIGHT), COLOR_BG_TOP)
    draw_gradient_bg(img)
    draw = ImageDraw.Draw(img)

    draw_header(draw, progress, "Grow Your Nepali Business")

    # Hero
    t_h = ease_out(min(1.0, (progress-0.08)*5))
    yo  = int(lerp(-60, 0, t_h))
    draw.text((540, 255+yo), "Is your business listed on",
              font=get_font(40), fill=COLOR_MUTED, anchor="mm")
    draw.text((540, 310+yo), "NepState?", font=get_font(68, bold=True),
              fill=COLOR_RED, anchor="mm")
    draw.text((540, 375+yo), "Reach thousands of Nepalis near you 🎯",
              font=get_font(34), fill=COLOR_GOLD_LIGHT, anchor="mm")

    # Benefit rows
    row_top = 430
    row_h   = 185
    pad     = 50

    for idx, (emoji, title, desc) in enumerate(BENEFITS):
        delay = 0.04 * idx
        t = ease_out(min(1.0, max(0.0, (progress - 0.12 - delay) * 4)))
        slide = int(lerp(-VIDEO_WIDTH, 0, t))

        top = row_top + idx * row_h
        bot = top + row_h - 14

        # Alternating card shades
        bg = (32, 20, 20) if idx % 2 == 0 else (24, 15, 15)
        draw_rounded_rect(draw, [pad+slide, top, VIDEO_WIDTH-pad+slide, bot],
                          18, bg, outline=COLOR_RED, outline_width=2)

        draw.text((pad + 70 + slide, top + (row_h-14)//2), emoji,
                  font=get_font(46), anchor="mm")
        draw.text((pad + 140 + slide, top + 44), title,
                  font=get_font(38, bold=True), fill=COLOR_WHITE, anchor="lm")
        for li, line in enumerate(desc.split("\n")):
            draw.text((pad + 140 + slide, top + 92 + li*36), line,
                      font=get_font(28), fill=COLOR_MUTED, anchor="lm")

        # Checkmark
        draw.text((VIDEO_WIDTH - pad - 40 + slide, top + (row_h-14)//2),
                  "✓", font=get_font(44, bold=True), fill=COLOR_GREEN, anchor="mm")

    draw_cta(draw, progress, cta_text="Add your business FREE →")
    return img

def get_caption():
    return """\
🏢 Nepali Business Owners — Get Discovered for FREE on NepState!

✅ Free business listing
✅ Customer reviews & ratings
✅ Phone, WhatsApp & email on your profile
✅ Business hours & photo gallery
✅ Spotlight options for maximum visibility

Thousands of Nepalis search NepState every month.
Don't miss out — list your business today!

👉 nepstate.com/add-business

#NepStateBusiness #NepaliBusinessUSA #NepaliEntrepreneur
#NepaliRestaurant #NepaliUSA #SmallBusiness #NepaliCommunity"""

def run():
    print("🎬 Generating: For Businesses")
    os.makedirs(FRAMES_DIR, exist_ok=True)
    total = FPS * DURATION
    for i in range(total):
        generate_frame(i, total).save(f"{FRAMES_DIR}/frame_{i:04d}.png")
        if i % 60 == 0: print(f"   {i}/{total} frames...")
    return compile_video(OUTPUT), get_caption()

if __name__ == "__main__":
    run()
