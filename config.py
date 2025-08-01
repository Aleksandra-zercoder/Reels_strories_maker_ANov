from dotenv import load_dotenv
import os

load_dotenv()

# Безопасные настройки
FRAME_DURATION = 4
VIDEO_RESOLUTION = (1080, 1920)
FPS = 30
BACKGROUND_COLOR = "white"

# Секреты из .env
IAM_TOKEN = os.getenv("IAM_TOKEN")
FOLDER_ID = os.getenv("FOLDER_ID")
OAUTH_TOKEN = os.getenv("OAUTH_TOKEN")
JAMENDO_CLIENT_ID = os.getenv("JAMENDO_CLIENT_ID")


# Видео
FRAME_DURATION = 4  # длительность одного изображения в секундах
VIDEO_RESOLUTION = (1080, 1920)
FPS = 30
BACKGROUND_COLOR = "white"  # можно заменить на (R, G, B)
