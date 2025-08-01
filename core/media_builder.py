from moviepy.editor import (
    ImageClip,
    VideoFileClip,
    concatenate_videoclips,
    TextClip,
    CompositeVideoClip
)
from PIL import Image, ImageFilter
import os
from config import FRAME_DURATION, FPS, VIDEO_RESOLUTION, BACKGROUND_COLOR


def process_image_with_fit(path, mode="cover", output_size=VIDEO_RESOLUTION, background_color=BACKGROUND_COLOR):
    original = Image.open(path).convert("RGB")

    if mode == "center":
        original.thumbnail(output_size, Image.Resampling.LANCZOS)
        background = Image.new("RGB", output_size, background_color)
        x = (output_size[0] - original.width) // 2
        y = (output_size[1] - original.height) // 2
        background.paste(original, (x, y))
        return background

    elif mode == "cover":
        iw, ih = original.size
        ow, oh = output_size
        ratio = max(ow / iw, oh / ih)
        new_size = (int(iw * ratio), int(ih * ratio))
        resized = original.resize(new_size, Image.Resampling.LANCZOS)
        left = (resized.width - ow) // 2
        top = (resized.height - oh) // 2
        right = left + ow
        bottom = top + oh
        return resized.crop((left, top, right, bottom))

    elif mode == "blur":
        blurred = original.resize(output_size, Image.Resampling.LANCZOS).filter(ImageFilter.GaussianBlur(20))
        original.thumbnail(output_size, Image.Resampling.LANCZOS)
        x = (output_size[0] - original.width) // 2
        y = (output_size[1] - original.height) // 2
        blurred.paste(original, (x, y))
        return blurred

    else:
        raise ValueError(f"Unknown fit mode: {mode}")


def build_video_from_media(media_folder, slide_texts=None, fit_mode="cover", logo_path=None, logo_size=100, caption=None):
    media_files = sorted([
        os.path.join(media_folder, f)
        for f in os.listdir(media_folder)
        if f.lower().endswith((".jpg", ".jpeg", ".png", ".mp4"))
    ])

    clips = []

    for i, path in enumerate(media_files):
        ext = os.path.splitext(path)[1].lower()

        # Базовый клип
        if ext in [".jpg", ".jpeg", ".png"]:
            img = process_image_with_fit(path, mode=fit_mode)
            temp_path = f"output/__temp_{i:03}.jpg"
            os.makedirs("output", exist_ok=True)
            img.save(temp_path)
            base = ImageClip(temp_path, duration=FRAME_DURATION)
        elif ext == ".mp4":
            base = VideoFileClip(path).resize(height=VIDEO_RESOLUTION[1])
        else:
            continue

        base = base.set_fps(FPS)
        overlays = [base]

        # Постоянный caption для всех кадров
        if caption:
            txt = (
                TextClip(caption.strip(), fontsize=48, color="white", font="Arial", method="caption")
                .set_duration(base.duration)
                .set_position(("center", "bottom"))
                .margin(bottom=60, opacity=0)
            )
            overlays.append(txt)

        # Логотип
        if logo_path and os.path.exists(logo_path):
            logo = (
                ImageClip(logo_path)
                .set_duration(base.duration)
                .resize(height=int(logo_size))
                .set_position(("right", "top"))
                .margin(top=20, right=20, opacity=0)
            )
            overlays.append(logo)

        final = CompositeVideoClip(overlays)
        clips.append(final)

    return concatenate_videoclips(clips, method="compose")
