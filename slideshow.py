from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip
from moviepy.video.fx.all import fadein

# Sample Data (Replace this with actual word timestamps)
words = [
    {"text": "Hello", "start": 1.0, "end": 1.5},
    {"text": "world", "start": 1.6, "end": 2.0},
    {"text": "this", "start": 2.1, "end": 2.5},
    {"text": "is", "start": 2.6, "end": 3.0},
    {"text": "cool!", "start": 3.1, "end": 3.5}
]

# Load video
video = VideoFileClip("input_video.mp4")

# Create animated captions
text_clips = []
for word in words:
    txt_clip = (TextClip(word["text"], fontsize=70, color="white", font="Arial-Bold")
                .set_position(("center", "bottom"))
                .set_start(word["start"])
                .set_duration(word["end"] - word["start"])
                .fx(fadein, 0.3))  # Pop-in effect
    
    text_clips.append(txt_clip)

# Overlay text on video
final = CompositeVideoClip([video] + text_clips)

# Output
final.write_videofile("output_video.mp4", fps=video.fps)
