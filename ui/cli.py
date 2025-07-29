import argparse

def get_args():
    parser = argparse.ArgumentParser(description="Генератор вертикальных видео из изображений и музыки.")
    parser.add_argument("--images", type=str, help="Путь к папке с изображениями")
    parser.add_argument("--audio", type=str, help="Путь к аудиофайлу")
    parser.add_argument("--output", type=str, default="output/video.mp4", help="Путь сохранения видео")
    parser.add_argument("--fit_mode", type=str, default="center",
                        choices=["center", "cover", "blur"],
                        help="Способ подгонки изображения: center / cover / blur")
    parser.add_argument("--preview", action="store_true", help="Показать предпросмотр первого кадра")
    parser.add_argument("--clean", action="store_true", help="Удалить временные файлы после генерации")
    parser.add_argument("--name", type=str, help="Имя итогового файла (без .mp4)")
    parser.add_argument("--logo", type=str, help="Путь к логотипу PNG или JPG")
    parser.add_argument("--logo_size", type=int, default=100, help="Высота логотипа в пикселях (по умолчанию: 100)")
    parser.add_argument("--caption", type=str, help="Текст, который отобразится на видео")
    return parser.parse_args()



