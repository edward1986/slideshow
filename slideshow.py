import os
import requests
from moviepy.editor import *

# Configuration
IMAGE_FOLDER = "images"
OUTPUT_VIDEO = "slideshow_with_scrolling_subtitles.mp4"
DURATION = 60
FPS = 30
RESOLUTION = (1080, 1920)

# Sample Scrolling Subtitle Data (timestamps removed)
subtitle_text = """ 
Welcome to an amazing journey!
This is a futuristic city at night.
A sunset over the ocean, calm and peaceful.
Snow-covered mountains, reaching high.
A fantasy castle floating in the sky.
Neon cyberpunk streets full of energy.
A forest with a peaceful river.
The journey continues...
"""

# ✅ Generate a Single Scrolling Subtitle Block
def create_scrolling_subtitles():
    """Creates a smoothly scrolling subtitle effect"""
    
    # Create a TextClip with multiline subtitles
    txt_clip = TextClip(
        subtitle_text,
        fontsize=50,
        font="Arial-Bold",
        color="white",
        stroke_color="black",
        stroke_width=2,
        method="caption",
        size=(800, None),  # Adjust width to fit screen
    )
    
    # Position at the bottom initially, then move up
    scrolling_subtitles = txt_clip.set_position(("center", 1920)).set_duration(DURATION)
    
    # Animate scrolling upwards
    return scrolling_subtitles.set_position(lambda t: ("center", 1920 - (t * 100)))

# ✅ Generate scrolling subtitles
scrolling_subtitles = create_scrolling_subtitles()

# ✅ Load images for the slideshow
images = [os.path.join(IMAGE_FOLDER, img) for img in sorted(os.listdir(IMAGE_FOLDER)) if img.endswith(".jpg")]
image_duration = DURATION / len(images)
clip = ImageSequenceClip(images, durations=[image_duration] * len(images))

# ✅ Resize and crop for YouTube Shorts
vertical_clip = clip.resize(height=1920).crop(x_center=clip.w // 2, width=1080, height=1920)

# ✅ Combine Video & Scrolling Subtitles
final_clip = CompositeVideoClip([vertical_clip, scrolling_subtitles])

# ✅ Export final video
final_clip.write_videofile(OUTPUT_VIDEO, fps=FPS)

print("🎬 Slideshow video with scrolling subtitles generated successfully!")
