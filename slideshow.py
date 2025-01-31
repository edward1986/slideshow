import os
import requests
from moviepy.editor import ImageSequenceClip

IMAGE_FOLDER = "images"
OUTPUT_VIDEO = "slideshow.mp4"
DURATION = 60  # Total video duration in seconds
FPS = 24  # Frames per second
NUM_IMAGES = 6  # Number of images for the slideshow

# Create the images directory if it doesn't exist
os.makedirs(IMAGE_FOLDER, exist_ok=True)

def download_image(prompt, index):
    """Download an AI-generated image from Pollinations"""
    width, height, seed, model = 1024, 1024, 42, "flux"
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

# Create slideshow
images = [os.path.join(IMAGE_FOLDER, img) for img in sorted(os.listdir(IMAGE_FOLDER)) if img.endswith(".jpg")]
image_duration = DURATION / len(images)

clip = ImageSequenceClip(images, durations=[image_duration] * len(images))
clip.write_videofile(OUTPUT_VIDEO, fps=FPS)

print("🎬 Slideshow video generated successfully!")
