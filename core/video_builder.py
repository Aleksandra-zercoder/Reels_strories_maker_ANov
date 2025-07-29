from moviepy.editor import (
    ImageClip,
    TextClip,
    CompositeVideoClip,
    concatenate_videoclips
)
import os
from config import FRAME_DURATION, FPS, VIDEO_RESOLUTION

def build_video_from_images(image_paths, logo_path=None, caption=None, logo_size=100):
    clips = []

    for path in image_paths:
        base_clip = ImageClip(path, duration=FRAME_DURATION)
        base_clip = base_clip.set_fps(FPS)

        overlays = [base_clip]

        # Логотип в правом верхнем углу
        if logo_path and os.path.exists(logo_path):
            logo = (
                ImageClip(logo_path)
                .set_duration(FRAME_DURATION)
                .resize(height=logo_size)
                .set_position(("right", "top"))
                .margin(top=40, right=40, opacity=0)
            )
            overlays.append(logo)

        # Подпись внизу по центру
        if caption:
            txt = (
                TextClip(caption, fontsize=48, color="white", font="Arial-Bold")
                .set_duration(FRAME_DURATION)
                .set_position(("center", "bottom"))
                .margin(bottom=80, opacity=0)
                .fadein(0.3)
            )
            overlays.append(txt)

        final = CompositeVideoClip(overlays)
        clips.append(final)

    return concatenate_videoclips(clips, method="compose")
