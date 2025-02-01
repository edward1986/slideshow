import os
import requests
import random  # Import random module
from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip
from moviepy.video.fx.all import fadein, fadeout




IMAGE_FOLDER = "images"
OUTPUT_VIDEO = "slideshow_shorts.mp4"
DURATION = 60  # Total video duration in seconds
FPS = 30  # 30 FPS is recommended for YouTube Shorts
ZOOM_FACTOR = 1.2  # 20% zoom
RESOLUTION = (1080, 1920)  # YouTube Shorts Vertical Resolution

# Create the images directory if it doesn't exist
os.makedirs(IMAGE_FOLDER, exist_ok=True)

def download_image(prompt, index):
    """Download an AI-generated image from Pollinations"""
    width, height, seed, model = 1920, 1080, 42, "flux"  # Use 16:9 images
    image_url = f"https://pollinations.ai/p/{prompt}?width={width}&height={height}&seed={seed}&model={model}"
    image_path = os.path.join(IMAGE_FOLDER, f"image_{index}.jpg")

    response = requests.get(image_url)
    if response.status_code == 200:
        with open(image_path, "wb") as file:
            file.write(response.content)
        print(f"Downloaded {image_path}")
    else:
        print(f"Failed to download image {index}")

# Generate and download images
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

# Load images and create the base slideshow
images = [os.path.join(IMAGE_FOLDER, img) for img in sorted(os.listdir(IMAGE_FOLDER)) if img.endswith(".jpg")]
image_duration = DURATION / len(images)

clip = ImageSequenceClip(images, durations=[image_duration] * len(images))

# Resize and crop to 1080x1920 for YouTube Shorts
vertical_clip = clip.resize(height=1920).crop(x_center=clip.w // 2, width=1080, height=1920)

# ✅ Add Slow Zoom Effect for Shorts
zoomed_clip = vertical_clip.fx(vfx.resize, lambda t: 1 + (ZOOM_FACTOR - 1) * (t / clip.duration))

# Export final video
zoomed_clip.write_videofile(OUTPUT_VIDEO, fps=FPS)



# Load video (Replace with your actual video file)
video = VideoFileClip("slideshow_shorts.mp4")  # Change this to your file

# Simulated word timestamps (Customize as needed)
word_timestamps = [
    {"word": "Hello", "start": 1.0, "end": 1.5, "color": "yellow"},
    {"word": "world,", "start": 1.6, "end": 2.0, "color": "cyan"},
    {"word": "this", "start": 2.1, "end": 2.5, "color": "magenta"},
    {"word": "is", "start": 2.6, "end": 3.0, "color": "red"},
    {"word": "MoviePy!", "start": 3.1, "end": 3.5, "color": "lime"}
]

# Get video dimensions
W, H = video.size  # Width, Height of the video

# List of Montserrat font variations
fontlist = [
    "Montserrat-Black", "Montserrat-BlackItalic", "Montserrat-Bold", "Montserrat-BoldItalic",
    "Montserrat-ExtraBold", "Montserrat-ExtraBoldItalic", "Montserrat-ExtraLight",
    "Montserrat-ExtraLightItalic", "Montserrat-Italic", "Montserrat-Light", "Montserrat-LightItalic",
    "Montserrat-Medium", "Montserrat-MediumItalic", "Montserrat-Regular", "Montserrat-SemiBold",
    "Montserrat-SemiBoldItalic", "Montserrat-Thin", "Montserrat-ThinItalic"
]

# Generate pop-in animated text clips with bounce effect
text_clips = []
for word in word_timestamps:
    fontname = random.choice(fontlist)  # Randomly select a font
    
    txt_clip = (TextClip(word["word"], fontsize=130, color=word["color"], font=fontname, stroke_color="black", stroke_width=6)
                .set_position(("center", "center"))  # Centering text
                .set_start(word["start"])
                .set_duration(word["end"] - word["start"])
                .fx(fadein, 0.2)
                .fx(fadeout, 0.2))  # Smooth in & out
    
    # Scale up slightly for a "bounce" effect
    txt_clip = txt_clip.resize(lambda t: 1.3 if t - word["start"] < 0.15 else 1.0)
    
    text_clips.append(txt_clip)

# Overlay text on video
final = CompositeVideoClip([video] + text_clips)

# Export final video
final.write_videofile("output_stylish_captions.mp4", fps=video.fps, codec="libx264", audio_codec="aac")

print("Video with animated, stylish captions is ready!")
