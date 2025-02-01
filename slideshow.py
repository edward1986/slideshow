import os
import subprocess  # Import subprocess to run FFmpeg
import requests
import random  # Import random module
from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip, ImageSequenceClip, vfx
from moviepy.video.fx.all import fadein, fadeout

IMAGE_FOLDER = "images"
OUTPUT_VIDEO = "slideshow_shorts.mp4"
COMPRESSED_VIDEO = "slideshow_shorts_compressed.mp4"  # Compressed output filename
DURATION = 60  # Total video duration in seconds
FPS = 30  # 30 FPS is recommended for YouTube Shorts
ZOOM_FACTOR = 1.2  # 20% zoom
RESOLUTION = (720, 1280) # Lower resolution for smaller file size

# Create the images directory if it doesn't exist
os.makedirs(IMAGE_FOLDER, exist_ok=True)

# ✅ Load video and add captions (As in your original script)
video = VideoFileClip(OUTPUT_VIDEO)

# Simulated word timestamps (Customize as needed)
word_timestamps = [
    {"word": "Hello", "start": 1.0, "end": 1.5, "color": "yellow"},
    {"word": "world,", "start": 1.6, "end": 2.0, "color": "cyan"},
    {"word": "this", "start": 2.1, "end": 2.5, "color": "magenta"},
    {"word": "is", "start": 2.6, "end": 3.0, "color": "red"},
    {"word": "MoviePy!", "start": 3.1, "end": 3.5, "color": "lime"}
]

# Overlay text on video
final = CompositeVideoClip([video])

# ✅ Export final video (before compression)
final.write_videofile(OUTPUT_VIDEO, fps=video.fps, codec="libx264", audio_codec="aac")

print("✅ Video with animated, stylish captions is ready!")

# ✅ **Compress the video using FFmpeg**
compression_command = [
    "ffmpeg", "-i", OUTPUT_VIDEO,   # Input video
    "-vcodec", "libx265", "-crf", "28",  # H.265 codec with a high compression rate
    "-preset", "slow",  # Slower compression for better quality
    "-b:v", "500k",  # Limit video bitrate to 500kbps
    "-bufsize", "1000k",  # Buffer size
    "-maxrate", "800k",  # Maximum bitrate
    "-acodec", "aac", "-b:a", "128k",  # Audio compression
    COMPRESSED_VIDEO  # Output filename
]

# Run FFmpeg compression
subprocess.run(compression_command, check=True)

print(f"✅ Compression complete! Saved as {COMPRESSED_VIDEO}")
