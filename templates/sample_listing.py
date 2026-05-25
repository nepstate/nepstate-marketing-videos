"""
Template: SAMPLE LISTING
Saturday video — shows what a listing looks like, drives posting.
Rotates between Event / Job / Housing each week.
"""
import sys, os, math
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from PIL import Image, ImageDraw
from common import *
from datetime import datetime

OUTPUT = "marketing-video.mp4"

# Rotate sample type by week number
WEEK = datetime.now().isocalendar()[1]
SAMPLE_TYPE = ["event", "job", "housing"][WEEK % 3]

SAMPLES = {
    "event": {
        "badge": "🎉 EVENT",
        "badge_color": COLOR_RED,
        "title": "Nepali New Year Celebration 2082",
        "fields": [
            ("📅", "Date",     "April 13, 2026 • Saturday"),
            ("🕐", "Time",     "6:00 PM — 11:00 PM"),
            ("📍", "Location", "Community Center, Dallas TX"),
            ("🎫", "Tickets",  "$15 Adults • $8 Kids"),
            ("📞", "Contact",  "+1 (214) 555-0182"),
        ],
        "desc": "Join us for an unforgettable Nepali New Year\ncelebration with music, dance, food & culture!",
        "cta": "Post your event FREE →",
        "caption_hook": "🎉 Hosting a Nepali event? List it FREE on NepState!\nThis is what your listing looks like:",
        "hashtags": "#NepaliEvent #NepaliUSA #NepaliNewYear #NepState",
    },
    "job": {
        "badge": "💼 JOB",
        "badge_color": (37, 99, 235),
        "title": "Software Engineer — Nepali Tech Company",
        "fields": [
            ("🏢", "Company",  "TechNepal Solutions Inc."),
            ("📍", "Location", "Dallas, TX (Remote OK)"),
            ("💰", "Salary",   "$90,000 — $130,000 / year"),
            ("📋", "Type",     "Full-time • W2"),
            ("✉️", "Apply",    "jobs@technepal.com"),
        ],
        "desc": "Looking for a skilled software engineer\nwho understands the Nepali community!",
        "cta": "Post your job FREE →",
        "caption_hook": "💼 Hiring? Post your job FREE on NepState!\nThis is what your listing looks like:",
        "hashtags": "#NepaliJobs #NepaliUSA #NepaliTech #NepState #HiringNow",
    },
    "housing": {
        "badge": "🏠 HOUSING",
        "badge_color": COLOR_GREEN,
        "title": "Private Room for Rent — Nepali Household",
        "fields": [
            ("📍", "Location", "Irving, TX (near DFW)"),
            ("💵", "Rent",     "$650 / month + utilities"),
            ("🛏️", "Room",     "Private room, shared bath"),
            ("📅", "Available","June 1, 2026"),
            ("📞", "Contact",  "+1 (972) 555-0147"),
        ],
        "desc": "Nepali household, vegetarian preferred.\nClose to temple, Indian grocery, bus stop.",
        "cta": "Post your room FREE →",
        "caption_hook": "🏠 Room for rent? Find a Nepali roommate FREE!\nThis is what your listing looks like:",
        "hashtags": "#NepaliHousing #NepaliRoommate #NepaliUSA #NepState",
    },
}

def generate_frame(i, total):
    progress = i / total
    s = SAMPLES[SAMPLE_TYPE]
    img = Image.new('RGB', (VIDEO_WIDTH, VIDEO_HEIGHT), COLOR_BG_TOP)
    draw_gradient_bg(img)
    draw = ImageDraw.Draw(img)

    draw_header(draw, progress, "See how easy it is to post!")

    # Intro text
    t_intro = ease_out(min(1.0, (progress - 0.08) * 5))
    iy = int(lerp(-40, 0, t_intro))
    draw.text((540, 255+iy), "Sample listing on NepState:",
              font=get_font(38), fill=COLOR_MUTED, anchor="mm")

    # Main listing card
    t_card = ease_out(min(1.0, (progress - 0.15) * 3))
    cy = int(lerp(VIDEO_HEIGHT, 0, t_card))
    card_top = 305

    draw_rounded_rect(draw, [40, card_top+cy, 1040, 1700+cy], 28,
                      COLOR_CARD_DARK, outline=s["badge_color"], outline_width=3)

    # Badge
    t_badge = ease_out(min(1.0, (progress-0.25)*4))
    draw_rounded_rect(draw, [70, card_top+20+cy, 280, card_top+72+cy], 16, s["badge_color"])
    draw.text((175, card_top+46+cy), s["badge"],
              font=get_font(28, bold=True), fill=COLOR_WHITE, anchor="mm")

    # Community Listed badge
    draw_rounded_rect(draw, [720, card_top+20+cy, 1010, card_top+72+cy], 16, (40, 30, 10))
    draw.text((865, card_top+46+cy), "📢 Community Post",
              font=get_font(26, bold=True), fill=COLOR_GOLD, anchor="mm")

    # Title
    t_title = ease_out(min(1.0, (progress-0.28)*4))
    draw.text((80, card_top+100+cy), s["title"],
              font=get_font(40, bold=True), fill=COLOR_WHITE, anchor="lm")

    # Description
    for li, line in enumerate(s["desc"].split("\n")):
        draw.text((80, card_top+150+li*38+cy), line,
                  font=get_font(30), fill=COLOR_MUTED, anchor="lm")

    # Divider
    draw.rectangle([80, card_top+238+cy, 960, card_top+242+cy], fill=(50,35,35))

    # Fields
    for fi, (icon, label, val) in enumerate(s["fields"]):
        delay = 0.04 * fi
        t_f = ease_out(min(1.0, max(0.0, (progress - 0.32 - delay) * 4)))
        slide = int(lerp(-300, 0, t_f))
        fy = card_top + 265 + fi * 84 + cy
        draw.text((80+slide, fy+20), icon, font=get_font(34), anchor="lm")
        draw.text((130+slide, fy+5), label+":", font=get_font(26, bold=True),
                  fill=COLOR_MUTED, anchor="lm")
        draw.text((130+slide, fy+38), val, font=get_font(34, bold=True),
                  fill=COLOR_WHITE, anchor="lm")

    # Claim button mock
    t_btn = ease_out(min(1.0, max(0.0, (progress-0.55)*3)))
    bx = int(lerp(200, 0, t_btn))
    draw_rounded_rect(draw, [80+bx, card_top+705+cy, 520+bx, card_top+770+cy],
                      20, s["badge_color"])
    draw.text((300+bx, card_top+738+cy), "Contact Now",
              font=get_font(34, bold=True), fill=COLOR_WHITE, anchor="mm")
    draw_rounded_rect(draw, [540+bx, card_top+705+cy, 960+bx, card_top+770+cy],
                      20, (45, 30, 30))
    draw.text((750+bx, card_top+738+cy), "❤️ Save",
              font=get_font(34, bold=True), fill=COLOR_WHITE, anchor="mm")

    # Arrow pointing up + "Yours could look like this!"
    t_arrow = ease_out(max(0.0, (progress-0.6)*3))
    arrow_alpha = int(255 * t_arrow)
    draw.text((540, 1730), "☝️ Yours could look like this!",
              font=get_font(36, bold=True), fill=COLOR_GOLD_LIGHT, anchor="mm")

    draw_cta(draw, progress, cta_text=s["cta"])
    return img

def get_caption():
    s = SAMPLES[SAMPLE_TYPE]
    return f"""\
{s["caption_hook"]}

✅ Takes less than 2 minutes
✅ Reach thousands of Nepalis in the US
✅ 100% FREE — no hidden fees

👉 nepstate.com/post-listing

{s["hashtags"]} #NepaliCommunity #ConnectingNepaleseGlobally"""

def run():
    print(f"🎬 Generating: Sample Listing ({SAMPLE_TYPE})")
    os.makedirs(FRAMES_DIR, exist_ok=True)
    total = FPS * DURATION
    for i in range(total):
        generate_frame(i, total).save(f"{FRAMES_DIR}/frame_{i:04d}.png")
        if i % 60 == 0: print(f"   {i}/{total} frames...")
    return compile_video(OUTPUT), get_caption()

if __name__ == "__main__":
    run()
