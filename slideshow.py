from moviepy.editor import ImageSequenceClip, AudioFileClip
import os

# Define parameters
image_folder = "images"  # Folder containing images
output_video = "slideshow.mp4"
duration = 60  # Total video duration in seconds
fps = 24  # Frames per second

# Load images from folder
images = [os.path.join(image_folder, img) for img in sorted(os.listdir(image_folder)) if img.endswith((".png", ".jpg", ".jpeg"))]

# Determine duration per image
image_duration = duration / len(images)

# Create slideshow video
clip = ImageSequenceClip(images, durations=[image_duration] * len(images))

# Add background music (optional)
music_path = "background.mp3"  # Replace with your audio file
if os.path.exists(music_path):
    audio = AudioFileClip(music_path).set_duration(clip.duration)
    clip = clip.set_audio(audio)

# Export video
clip.write_videofile(output_video, fps=fps)
