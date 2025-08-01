from ui.cli import get_args
from core.media_builder import build_video_from_media
from core.audio_handler import prepare_audio
import os

def main():
    args = get_args()

    # Генерация видео из изображений и/или видеофрагментов
    video = build_video_from_media(
        media_folder=args.images,
        slide_texts=args.slide_texts,
        fit_mode=args.fit_mode,
        logo_path=args.logo,
        logo_size=int(args.logo_size),
        caption=args.caption  # 👈 важно
    )

    # Добавление аудио, если указано
    if args.audio:
        audio = prepare_audio(args.audio, video.duration)
        video = video.set_audio(audio)
        print("Аудио добавлено.")

    # Сохранение итогового видео
    output_path = f"output/{args.name}.mp4"
    os.makedirs("output", exist_ok=True)
    video.write_videofile(
        output_path,
        codec="libx264",
        audio_codec="aac",
        audio=True,
        temp_audiofile="temp-audio.m4a",  # Временный файл
        remove_temp=True,
        fps=30
    )
    print(f"Видео сохранено: {output_path}")

if __name__ == "__main__":
    main()

