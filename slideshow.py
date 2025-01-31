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

# ✅ Generate Scrolling Subtitle Clip
def create_scrolling_subtitles():
    """Creates a vertically scrolling subtitle effect"""
    subtitle_clips = []
    y_start = 1920  # Start position (off-screen)
    line_height = 80  # Distance between lines

    for i, (start_time, text) in enumerate(subtitles):
        txt_clip = TextClip(
            text, fontsize=60, font="Arial-Bold", color="white", stroke_color="black", stroke_width=3, method="caption"
        ).set_duration(15).set_position(("center", y_start - (i * line_height)))

        subtitle_clips.append(txt_clip)

    return CompositeVideoClip(subtitle_clips).set_duration(15).fx(vfx.scroll, 0, -600)

# ✅ Generate scrolling subtitles
scrolling_subtitles = create_scrolling_subtitles()

# ✅ Add to video
final_clip = CompositeVideoClip([zoomed_clip, scrolling_subtitles])

# ✅ Export final video
final_clip.write_videofile("slideshow_with_scrolling_subtitles.mp4", fps=30)

print("🎬 Slideshow video with scrolling subtitles generated successfully!")
