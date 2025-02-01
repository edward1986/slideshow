import os
import random  # Import random module
from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip
from moviepy.video.fx.all import fadein, fadeout

# Load video (Replace with your actual video file)
video = VideoFileClip("slideshow_shorts_compressed.mp4")  # Change this to your file

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
