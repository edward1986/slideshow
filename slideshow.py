from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip
from moviepy.video.fx.all import fadein, fadeout

# Load video (Replace with your actual video file)
video = VideoFileClip("shorts_with_bounce_captions.mp4")  # Change this to your file

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

# Choose a more stylish font
fontlist = [
    "Montserrat-Black.ttf", "Montserrat-BlackItalic.ttf", "Montserrat-Bold.ttf", "Montserrat-BoldItalic.ttf",
    "Montserrat-ExtraBold.ttf", "Montserrat-ExtraBoldItalic.ttf", "Montserrat-ExtraLight.ttf",
    "Montserrat-ExtraLightItalic.ttf", "Montserrat-Italic.ttf", "Montserrat-Light.ttf", "Montserrat-LightItalic.ttf",
    "Montserrat-Medium.ttf", "Montserrat-MediumItalic.ttf", "Montserrat-Regular.ttf", "Montserrat-SemiBold.ttf",
    "Montserrat-SemiBoldItalic.ttf", "Montserrat-Thin.ttf", "Montserrat-ThinItalic.ttf"
]

# Draw the signing name at the bottom
fontnumber = randint(0, 17)
fontname = fontlist[fontnumber]
font = ImageFont.truetype(os.path.join(os.getcwd(), "Font", fontname), 30)
signing_name = "QuoteEnlighten"  # Replace with the actual signing name
draw.text((760, 1000), signing_name, (50, 50, 50), font=font)

# Draw the quote text in the center
fontnumber2 = randint(0, 17)
fontname2 = fontlist[fontnumber2]
font = ImageFont.truetype(os.path.join(os.getcwd(), "Font", fontname2), 70)
max_width = 1000  # Set a max width for the text


# Generate pop-in animated text clips with bounce effect
text_clips = []
for word in word_timestamps:
    txt_clip = (TextClip(word["word"], fontsize=130, color=word["color"], font=font, stroke_color="black", stroke_width=6)
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
