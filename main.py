"""
NepState Marketing Video Orchestrator
Picks the correct template based on day of week and posts via Make.com.

Schedule:
  Monday    → Post for Free  (events / jobs / housing / directory)
  Tuesday   → [Gold/Silver — handled by separate repo]
  Wednesday → For Businesses
  Thursday  → [Forex — handled by separate repo]
  Friday    → What is NepState
  Saturday  → Sample Listing  (rotates: event / job / housing each week)
  Sunday    → Business Spotlight (rotates category each week)
"""

import os, sys, shutil
from datetime import datetime

MAKE_WEBHOOK_URL = os.environ.get("MAKE_MARKETING_WEBHOOK_URL", "")

def cleanup_frames():
    if os.path.exists("frames"):
        shutil.rmtree("frames")
        print("🧹 Cleaned up frames")

def main():
    day = datetime.now().weekday()   # 0=Mon … 6=Sun
    day_names = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
    print("=" * 55)
    print(f"🇳🇵 NepState Marketing Video Pipeline")
    print(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M')} — {day_names[day]}")
    print("=" * 55)

    # Select template
    if day == 0:
        from templates.post_for_free import run
        template_name = "Post For Free"
    elif day == 2:
        from templates.for_businesses import run
        template_name = "For Businesses"
    elif day == 4:
        from templates.what_is_nepstate import run
        template_name = "What Is NepState"
    elif day == 5:
        from templates.sample_listing import run
        template_name = "Sample Listing"
    elif day == 6:
        from templates.business_spotlight import run
        template_name = "Business Spotlight"
    else:
        print(f"ℹ️  {day_names[day]} — no marketing video scheduled today.")
        print("   (Gold/Silver runs Tue, Forex runs Thu — separate repo)")
        sys.exit(0)

    print(f"🎬 Template: {template_name}")

    # Generate video
    success, caption = run()
    if not success:
        print("❌ Video generation failed.")
        cleanup_frames()
        sys.exit(1)

    # Post via Make.com
    from common import send_to_make
    posted = send_to_make("marketing-video.mp4", caption, MAKE_WEBHOOK_URL)

    cleanup_frames()

    print("\n" + "=" * 55)
    print("📊 RESULT")
    print("=" * 55)
    print(f"  Template : {template_name}")
    print(f"  Video    : {'✅ Generated' if success else '❌ Failed'}")
    print(f"  Posted   : {'✅ Sent to Make.com' if posted else '❌ Failed/Skipped'}")
    print("=" * 55)

    if not posted:
        sys.exit(1)

if __name__ == "__main__":
    main()
