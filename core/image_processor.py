from PIL import Image, ImageFilter
import os
from config import VIDEO_RESOLUTION, BACKGROUND_COLOR
from PIL import ImageDraw, ImageFont

def process_image(image_path, mode="center", output_size=VIDEO_RESOLUTION, background_color=BACKGROUND_COLOR):
    original = Image.open(image_path).convert("RGB")

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
        raise ValueError(f"Неподдерживаемый режим подгонки: {mode}")

def load_images_from_folder(folder_path):
    image_files = sorted([
        os.path.join(folder_path, f)
        for f in os.listdir(folder_path)
        if f.lower().endswith((".jpg", ".jpeg", ".png"))
    ])
    return image_files

def generate_cover(image_path, output_path="output/cover.jpg", logo_path=None, caption=None, logo_size=100):
    img = process_image(image_path, mode="cover")

    # Логотип
    if logo_path and os.path.exists(logo_path):
        logo = Image.open(logo_path).convert("RGBA")
        ratio = logo_size / logo.height
        new_size = (int(logo.width * ratio), logo_size)
        logo = logo.resize(new_size, Image.Resampling.LANCZOS)
        img.paste(logo, (img.width - logo.width - 40, 40), mask=logo)

    # Текст
    if caption:
        draw = ImageDraw.Draw(img)
        try:
            font = ImageFont.truetype("Arial.ttf", 60)
        except:
            font = ImageFont.load_default()

        text_w, text_h = draw.textsize(caption, font=font)
        x = (img.width - text_w) // 2
        y = img.height - text_h - 80

        # полупрозрачный фон под текст
        draw.rectangle(
            [x - 20, y - 20, x + text_w + 20, y + text_h + 20],
            fill=(0, 0, 0, 180)
        )

        draw.text((x, y), caption, fill="white", font=font)

    img.save(output_path)
    print(f"Обложка сохранена: {output_path}")