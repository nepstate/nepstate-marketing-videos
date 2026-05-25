"""
Shared utilities for NepState marketing video templates.
"""
from PIL import Image, ImageDraw, ImageFont
import math, os, subprocess, requests

VIDEO_WIDTH  = 1080
VIDEO_HEIGHT = 1920
FPS          = 30
DURATION     = 12
FRAMES_DIR   = "frames"

COLOR_BG_TOP    = (14, 10, 10)
COLOR_BG_BOTTOM = (6,  4,  4)
COLOR_RED       = (192, 57,  43)
COLOR_GOLD      = (212, 160, 23)
COLOR_GOLD_LIGHT= (255, 215, 80)
COLOR_WHITE     = (255, 255, 255)
COLOR_MUTED     = (160, 150, 140)
COLOR_CARD_DARK = (28,  18,  18)
COLOR_GREEN     = (22, 163, 74)
COLOR_BLUE      = (37, 99, 235)

def ease_out(t):
    return 1 - (1 - max(0.0, min(1.0, t))) ** 3

def lerp(a, b, t):
    return a + (b - a) * t

def draw_rounded_rect(draw, xy, radius, fill, outline=None, outline_width=2):
    x1, y1, x2, y2 = xy
    draw.rectangle([x1+radius, y1, x2-radius, y2], fill=fill)
    draw.rectangle([x1, y1+radius, x2, y2-radius], fill=fill)
    draw.ellipse([x1, y1, x1+radius*2, y1+radius*2], fill=fill)
    draw.ellipse([x2-radius*2, y1, x2, y1+radius*2], fill=fill)
    draw.ellipse([x1, y2-radius*2, x1+radius*2, y2], fill=fill)
    draw.ellipse([x2-radius*2, y2-radius*2, x2, y2], fill=fill)
    if outline:
        for i in range(outline_width):
            draw.rectangle([x1+i, y1+i, x2-i, y2-i], outline=outline)

def draw_gradient_bg(img):
    draw = ImageDraw.Draw(img)
    for y in range(VIDEO_HEIGHT):
        ratio = y / VIDEO_HEIGHT
        r = int(lerp(COLOR_BG_TOP[0], COLOR_BG_BOTTOM[0], ratio))
        g = int(lerp(COLOR_BG_TOP[1], COLOR_BG_BOTTOM[1], ratio))
        b = int(lerp(COLOR_BG_TOP[2], COLOR_BG_BOTTOM[2], ratio))
        draw.line([(0, y), (VIDEO_WIDTH, y)], fill=(r, g, b))

def draw_header(draw, progress, tagline="Connecting Nepalese Globally 🌏"):
    t = ease_out(min(1.0, progress * 5))
    y_off = int(lerp(-150, 0, t))
    draw.rectangle([0, y_off, VIDEO_WIDTH, y_off+8], fill=COLOR_RED)
    draw.text((540, y_off+90), "NepState", font=get_font(80, bold=True),
              fill=COLOR_RED, anchor="mm")
    draw.text((540, y_off+155), tagline, font=get_font(30), fill=COLOR_MUTED, anchor="mm")
    draw.rectangle([0, VIDEO_HEIGHT-8, VIDEO_WIDTH, VIDEO_HEIGHT], fill=COLOR_RED)
    pulse = int(3 + 2*math.sin(progress * math.pi * 4))
    draw.rectangle([0, 0, VIDEO_WIDTH-1, VIDEO_HEIGHT-1], outline=COLOR_RED, width=pulse)

def draw_cta(draw, progress, url="nepstate.com", cta_text="Visit us today!"):
    t = ease_out(max(0.0, (progress - 0.6) * 3))
    y_off = int(lerp(200, 0, t))
    draw_rounded_rect(draw, [60, 1720+y_off, 1020, 1870+y_off], 24, COLOR_RED)
    draw.text((540, 1765+y_off), cta_text, font=get_font(38, bold=True),
              fill=COLOR_WHITE, anchor="mm")
    draw.text((540, 1820+y_off), f"🌐 {url}", font=get_font(42, bold=True),
              fill=COLOR_GOLD_LIGHT, anchor="mm")

def get_font(size, bold=False):
    paths = [
        os.path.join("assets", "arial.ttf"),
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold
        else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf" if bold
        else "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
    ]
    for p in paths:
        try: return ImageFont.truetype(p, size)
        except: continue
    return ImageFont.load_default()

def get_nepali_font(size, bold=False):
    name = "NotoSansDevanagari-Bold.ttf" if bold else "NotoSansDevanagari-Regular.ttf"
    for p in [os.path.join("assets", name), f"/usr/share/fonts/truetype/noto/{name}"]:
        try: return ImageFont.truetype(p, size)
        except: continue
    return get_font(size, bold)

def compile_video(output_path="marketing-video.mp4"):
    print("🎞️  Compiling with FFmpeg...")
    music = os.path.join("assets", "background_music.mp3")
    if os.path.exists(music):
        cmd = ["ffmpeg", "-y", "-framerate", str(FPS),
               "-i", f"{FRAMES_DIR}/frame_%04d.png",
               "-stream_loop", "-1", "-i", music,
               "-c:v", "libx264", "-c:a", "aac", "-pix_fmt", "yuv420p",
               "-crf", "23", "-shortest",
               "-filter:a", "volume=0.25,afade=t=in:st=0:d=1,afade=t=out:st=11:d=1",
               "-movflags", "+faststart", output_path]
    else:
        cmd = ["ffmpeg", "-y", "-framerate", str(FPS),
               "-i", f"{FRAMES_DIR}/frame_%04d.png",
               "-c:v", "libx264", "-pix_fmt", "yuv420p",
               "-crf", "23", "-movflags", "+faststart", output_path]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        print(f"[ERROR] FFmpeg: {r.stderr[-400:]}")
        return False
    print(f"✅ Video: {output_path}")
    return True

def send_to_make(video_path, caption, webhook_url):
    if not webhook_url:
        print("⚠️  MAKE_WEBHOOK_URL not set — skipping")
        return False
    try:
        print("📤 Sending to Make.com...")
        with open(video_path, "rb") as f:
            res = requests.post(webhook_url,
                files={"video": (os.path.basename(video_path), f, "video/mp4")},
                data={"caption": caption}, timeout=120)
        if res.status_code == 200:
            print("✅ Sent to Make.com!")
            return True
        print(f"[ERROR] Make.com {res.status_code}: {res.text[:200]}")
        return False
    except Exception as e:
        print(f"[ERROR] Make.com: {e}")
        return False
