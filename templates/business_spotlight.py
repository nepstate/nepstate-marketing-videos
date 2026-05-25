"""
Template: BUSINESS SPOTLIGHT
Sunday video — rotating category spotlight (restaurants, lawyers, salons…)
"""
import sys, os, math
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from PIL import Image, ImageDraw
from common import *
from datetime import datetime

OUTPUT = "marketing-video.mp4"

WEEK = datetime.now().isocalendar()[1]

CATEGORIES = [
    {
        "emoji": "🍛",  "name": "Nepali Restaurants",
        "color": COLOR_RED,
        "features": ["Authentic dal bhat & momo", "Newari & Thakali cuisine",
                     "Party & catering services", "Verified reviews & hours"],
        "cta_url": "nepstate.com/directory/restaurants",
        "hashtags": "#NepaliRestaurant #NepaliFood #MomoUSA",
    },
    {
        "emoji": "⚖️", "name": "Nepali Lawyers",
        "color": (37, 99, 235),
        "features": ["Immigration & visa help", "Green card & citizenship",
                     "Business & tax law", "Free initial consultations"],
        "cta_url": "nepstate.com/directory/lawyers",
        "hashtags": "#NepaliLawyer #ImmigrationLawyer #NepaliUSA",
    },
    {
        "emoji": "💇", "name": "Nepali Beauty & Salons",
        "color": (168, 85, 247),
        "features": ["Bridal makeup & hair", "Mehndi & threading",
                     "Saree draping services", "Wedding party packages"],
        "cta_url": "nepstate.com/directory/beauty",
        "hashtags": "#NepaliSalon #NepaliBeauty #NepaliWedding",
    },
    {
        "emoji": "🛒", "name": "Nepali Grocery Stores",
        "color": COLOR_GREEN,
        "features": ["Dal, chiura & spices", "Fresh Nepali vegetables",
                     "Pooja & puja supplies", "Imported Nepali products"],
        "cta_url": "nepstate.com/directory/grocery",
        "hashtags": "#NepaliGrocery #NepaliStore #NepaliFood",
    },
    {
        "emoji": "💰", "name": "Nepali Tax & Accounting",
        "color": COLOR_GOLD,
        "features": ["ITIN & tax filing", "Small business accounting",
                     "FBAR & foreign income", "Affordable Nepali CPAs"],
        "cta_url": "nepstate.com/directory/tax",
        "hashtags": "#NepaliCPA #NepaliTax #TaxHelp",
    },
    {
        "emoji": "🏥", "name": "Nepali Medical & Health",
        "color": (239, 68, 68),
        "features": ["Nepali-speaking doctors", "Mental health services",
                     "Ayurvedic practitioners", "Dental & vision care"],
        "cta_url": "nepstate.com/directory/medical",
        "hashtags": "#NepaliDoctor #NepaliHealth #NepaliUSA",
    },
]

CAT = CATEGORIES[WEEK % len(CATEGORIES)]

def generate_frame(i, total):
    progress = i / total
    img = Image.new('RGB', (VIDEO_WIDTH, VIDEO_HEIGHT), COLOR_BG_TOP)
    draw_gradient_bg(img)
    draw = ImageDraw.Draw(img)

    draw_header(draw, progress, "Discover Nepali Businesses Near You")

    # Spotlight badge
    t_badge = ease_out(min(1.0, (progress-0.1)*5))
    by = int(lerp(-60, 0, t_badge))
    draw_rounded_rect(draw, [200, 245+by, 880, 305+by], 20, CAT["color"])
    draw.text((540, 275+by), "✨ SPOTLIGHT THIS WEEK",
              font=get_font(30, bold=True), fill=COLOR_WHITE, anchor="mm")

    # Category hero card
    t_hero = ease_out(min(1.0, (progress-0.15)*3))
    hy = int(lerp(300, 0, t_hero))
    draw_rounded_rect(draw, [50, 325+hy, 1030, 720+hy], 30,
                      COLOR_CARD_DARK, outline=CAT["color"], outline_width=4)

    # Big emoji
    draw.text((540, 465+hy), CAT["emoji"], font=get_font(120), anchor="mm")
    draw.text((540, 580+hy), CAT["name"],
              font=get_font(52, bold=True), fill=COLOR_WHITE, anchor="mm")
    draw.text((540, 635+hy), "on NepState",
              font=get_font(34), fill=CAT["color"], anchor="mm")
    draw.text((540, 685+hy), "nepstate.com",
              font=get_font(30), fill=COLOR_MUTED, anchor="mm")

    # Feature list
    feat_top = 750
    for fi, feat in enumerate(CAT["features"]):
        delay = 0.05 * fi
        t_f = ease_out(min(1.0, max(0.0, (progress-0.3-delay)*4)))
        fx = int(lerp(-VIDEO_WIDTH, 0, t_f))
        fy = feat_top + fi * 120
        draw_rounded_rect(draw, [50+fx, fy, 1030+fx, fy+100], 18,
                          COLOR_CARD_DARK, outline=CAT["color"], outline_width=2)
        draw.text((100+fx, fy+50), "✓", font=get_font(44, bold=True),
                  fill=CAT["color"], anchor="mm")
        draw.text((150+fx, fy+50), feat, font=get_font(38, bold=True),
                  fill=COLOR_WHITE, anchor="lm")

    # Find + List prompts
    t_bottom = ease_out(max(0.0, (progress-0.55)*3))
    boty = int(lerp(100, 0, t_bottom))
    prompt_top = 1250
    draw_rounded_rect(draw, [50, prompt_top+boty, 1030, prompt_top+120+boty],
                      20, (35, 22, 10), outline=COLOR_GOLD, outline_width=2)
    draw.text((540, prompt_top+60+boty),
              f"🔍 Find {CAT['name']} near you",
              font=get_font(36, bold=True), fill=COLOR_GOLD_LIGHT, anchor="mm")

    draw_rounded_rect(draw, [50, prompt_top+140+boty, 1030, prompt_top+260+boty],
                      20, (15, 30, 15), outline=COLOR_GREEN, outline_width=2)
    draw.text((540, prompt_top+185+boty), "🏢 Own one? List FREE →",
              font=get_font(36, bold=True), fill=COLOR_GREEN, anchor="mm")
    draw.text((540, prompt_top+230+boty), "nepstate.com/add-business",
              font=get_font(30), fill=COLOR_MUTED, anchor="mm")

    draw_cta(draw, progress, url=CAT["cta_url"], cta_text="Browse now →")
    return img

def get_caption():
    return f"""\
{CAT["emoji"]} Spotlight: {CAT["name"]} on NepState!

Looking for trusted {CAT["name"].lower()} in your city?
NepState has you covered 🇳🇵

✅ {CAT["features"][0]}
✅ {CAT["features"][1]}
✅ {CAT["features"][2]}
✅ {CAT["features"][3]}

🔍 Find one near you → {CAT["cta_url"]}
🏢 Own one? List your business FREE → nepstate.com/add-business

{CAT["hashtags"]} #NepState #NepaliCommunity #NepaliUSA"""

def run():
    print(f"🎬 Generating: Business Spotlight — {CAT['name']}")
    os.makedirs(FRAMES_DIR, exist_ok=True)
    total = FPS * DURATION
    for i in range(total):
        generate_frame(i, total).save(f"{FRAMES_DIR}/frame_{i:04d}.png")
        if i % 60 == 0: print(f"   {i}/{total} frames...")
    return compile_video(OUTPUT), get_caption()

if __name__ == "__main__":
    run()
