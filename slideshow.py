from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip
from moviepy.video.fx.all import fadein

# Load video (Replace with your actual video file)
video = VideoFileClip("shorts_with_bounce_captions.mp4")  # Change this to your file

# Simulated word timestamps (Manually define words & their start times)
word_timestamps = [
    {"word": "Hello", "start": 1.0, "end": 1.5},
    {"word": "world,", "start": 1.6, "end": 2.0},
    {"word": "this", "start": 2.1, "end": 2.5},
    {"word": "is", "start": 2.6, "end": 3.0},
    {"word": "MoviePy!", "start": 3.1, "end": 3.5}
]

# Get video dimensions
W, H = video.size  # Width, Height of the video

# Generate pop-in animated text clips (Centered in the middle)
text_clips = []
for word in word_timestamps:
    txt_clip = (TextClip(word["word"], fontsize=100, color="white", font="Arial-Bold")
                .set_position(("center", "center"))  # Centering text
                .set_start(word["start"])
                .set_duration(word["end"] - word["start"])
                .fx(fadein, 0.3))  # Pop-in effect
    
    text_clips.append(txt_clip)

# Overlay text on video
final = CompositeVideoClip([video] + text_clips)

# Export final video
final.write_videofile("output_centered_captions.mp4", fps=video.fps, codec="libx264", audio_codec="aac")

print("Video with centered animated captions is ready!")
