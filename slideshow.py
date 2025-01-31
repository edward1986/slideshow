import os
import requests
from moviepy.editor import *

# Configuration
IMAGE_FOLDER = "images"
OUTPUT_VIDEO = "shorts_with_bounce_captions.mp4"
DURATION = 60  # Adjust based on video length
FPS = 30
RESOLUTION = (1080, 1920)

# ✅ Captions (Start Time, End Time, Text)
captions = [
    (0, 3, "🚀 Welcome to an *amazing* journey!"),
    (3, 6, "🌆 A *futuristic* city at night."),
    (6, 9, "🌅 The *perfect* sunset over the ocean."),
    (9, 12, "🏔️ Snow-covered *mountains* reaching high."),
    (12, 15, "🏰 A *fantasy* castle in the sky."),
    (15, 18, "🌆 Cyberpunk streets *full of energy!*"),
    (18, 21, "🌲 A *peaceful* forest by the river."),
    (21, 24, "🎬 *The journey continues...*"),
]

# ✅ Bounce Effect Function
def bounce_effect(t):
    """Creates a bouncing motion for the text"""
    return ("center", 950 - 40 * abs((t % 0.6) - 0.3) * 5)  # Adjust bounce height

# ✅ Generate Captions with Bounce Animation
def create_bounce_captions():
    caption_clips = []
    for start, end, text in captions:
        txt_clip = TextClip(
            text,
            fontsize=80,
            font="Arial-Bold",
            color="white",
            stroke_color="black",
            stroke_width=5,
            method="caption",
            size=(900, None),  # Wide enough for easy reading
        ).set_position(bounce_effect).set_start(start).set_end(end).fadein(0.5).fadeout(0.5)

        caption_clips.append(txt_clip)
    
    return CompositeVideoClip(caption_clips)

# ✅ Generate captions with bounce effect
captions_clip = create_bounce_captions()

# ✅ Load images for the slideshow
images = [os.path.join(IMAGE_FOLDER, img) for img in sorted(os.listdir(IMAGE_FOLDER)) if img.endswith(".jpg")]
image_duration = DURATION / len(images)
clip = ImageSequenceClip(images, durations=[image_duration] * len(images))

# ✅ Resize and crop for YouTube Shorts, TikTok, Reels
vertical_clip = clip.resize(height=1920).crop(x_center=clip.w // 2, width=1080, height=1920)

# ✅ Combine Video & Captions
final_clip = CompositeVideoClip([vertical_clip, captions_clip])

# ✅ Export final video
final_clip.write_videofile(OUTPUT_VIDEO, fps=FPS)

print("🎬 Short-form video with BOUNCE captions generated successfully!")
