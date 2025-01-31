import os
import requests
from moviepy.editor import *
from moviepy.video.tools.subtitles import SubtitlesClip

# Configuration
IMAGE_FOLDER = "images"
OUTPUT_VIDEO = "slideshow_with_subtitles.mp4"
DURATION = 60
FPS = 30
ZOOM_FACTOR = 1.2
RESOLUTION = (1080, 1920)

# Create the images directory if it doesn't exist
os.makedirs(IMAGE_FOLDER, exist_ok=True)

# Sample Subtitle Data (time_start, time_end, text)
subtitles = [
    ((0, 5), "Welcome to an amazing journey!"),
    ((5, 10), "This is a futuristic city at night."),
    ((10, 15), "A sunset over the ocean, calm and peaceful."),
    ((15, 20), "Snow-covered mountains, reaching high."),
    ((20, 25), "A fantasy castle floating in the sky."),
    ((25, 30), "Neon cyberpunk streets full of energy."),
    ((30, 35), "A forest with a peaceful river."),
    ((35, 40), "The journey continues..."),
]

# Download images
def download_image(prompt, index):
    """Download an AI-generated image"""
    width, height, seed, model = 1920, 1080, 42, "flux"
    image_url = f"https://pollinations.ai/p/{prompt}?width={width}&height={height}&seed={seed}&model={model}"
    image_path = os.path.join(IMAGE_FOLDER, f"image_{index}.jpg")

    response = requests.get(image_url)
    if response.status_code == 200:
        with open(image_path, "wb") as file:
            file.write(response.content)
        print(f"Downloaded {image_path}")
    else:
        print(f"Failed to download image {index}")

# Prompts
prompts = [
    "A futuristic city at night",
    "A sunset over the ocean",
    "A snow-covered mountain",
    "A fantasy castle in the sky",
    "A cyberpunk street with neon lights",
    "A peaceful forest with a river"
]

for i, prompt in enumerate(prompts):
    download_image(prompt, i)

# Load images
images = [os.path.join(IMAGE_FOLDER, img) for img in sorted(os.listdir(IMAGE_FOLDER)) if img.endswith(".jpg")]
image_duration = DURATION / len(images)
clip = ImageSequenceClip(images, durations=[image_duration] * len(images))

# Resize and crop for YouTube Shorts
vertical_clip = clip.resize(height=1920).crop(x_center=clip.w // 2, width=1080, height=1920)

# ✅ Slow Zoom Effect
zoomed_clip = vertical_clip.fx(vfx.resize, lambda t: 1 + (ZOOM_FACTOR - 1) * (t / clip.duration))

def subtitle_generator(txt):
    """Stylish text effect for subtitles"""
    return TextClip(txt, fontsize=60, font="Arial-Bold", color="white", stroke_color="black", stroke_width=3)

# ✅ Use a lambda function to avoid TypeError
subtitles_clip = SubtitlesClip(subtitles, make_textclip=lambda txt: subtitle_generator(txt))

# ✅ Position subtitles at the bottom and fade-in effect
styled_subtitles = subtitles_clip.set_position(("center", "bottom")).fadein(0.5)

# ✅ Combine Video & Subtitles
final_clip = CompositeVideoClip([zoomed_clip, styled_subtitles])

# Export final video
final_clip.write_videofile(OUTPUT_VIDEO, fps=FPS)
