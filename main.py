from ui.cli import get_args
from core.image_processor import load_images_from_folder, process_image
from core.video_builder import build_video_from_images
from core.audio_handler import prepare_audio
from PIL import Image
import os
import platform
import subprocess
import shutil
from core.image_processor import generate_cover

def open_preview_folder(folder_path):
    system = platform.system()
    if system == "Darwin":
        subprocess.call(["open", folder_path])
    elif system == "Windows":
        subprocess.call(["explorer", folder_path])
    elif system == "Linux":
        subprocess.call(["xdg-open", folder_path])

def main():
    args = get_args()

    if not args.images:
        print("Укажите путь к папке с изображениями")
        return

    os.makedirs("output/temp", exist_ok=True)

    images = load_images_from_folder(args.images)
    temp_image_paths = []

    for i, img_path in enumerate(images):
        img = process_image(img_path, mode=args.fit_mode)
        temp_path = f"output/temp/frame_{i:03}.jpg"
        img.save(temp_path)
        temp_image_paths.append(temp_path)

    print("Изображения обработаны.")
    if args.preview:
        Image.open(temp_image_paths[0]).show()

    open_preview_folder("output/temp")

    video = build_video_from_images(
        temp_image_paths,
        logo_path=args.logo,
        caption=args.caption,
        logo_size=args.logo_size
    )

    if args.audio:
        audio = prepare_audio(args.audio, video.duration)
        video = video.set_audio(audio)
        print("Аудио добавлено.")

    generate_cover(
        image_path=temp_image_paths[0],
        logo_path=args.logo,
        caption=args.caption,
        logo_size=args.logo_size
    )

    output_path = args.output
    if args.name:
        output_path = os.path.join("output", f"{args.name}.mp4")

    video.write_videofile(output_path, codec="libx264", fps=30)
    print(f"Видео сохранено: {output_path}")

    if args.clean:
        shutil.rmtree("output/temp")
        print("Временные файлы удалены.")

if __name__ == "__main__":
    main()

