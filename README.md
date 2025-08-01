# Reels Stories Maker (by A. Nov)

**Reels Stories Maker** — это инструмент для автоматизированного создания вертикальных видео (Reels/Stories) с генерацией изображений, наложением текста, логотипа и подбором музыки.

Проект поддерживает три способа взаимодействия:
- Консоль (CLI)
- Графический интерфейс (PyQt5)
- Веб-интерфейс (Flask)

---

## Возможности

- Генерация изображений через Yandex Art API
- Подбор музыки через Jamendo API
- Наложение текста и логотипа
- Объединение в вертикальный видеоролик
- Три интерфейса на выбор: CLI / GUI / Web

---

## Установка

1. Клонируйте репозиторий и установите зависимости:
```bash
git clone https://github.com/yourusername/ReelsStoriesMaker.git
cd ReelsStoriesMaker
pip install -r requirements.txt
```

2. Создайте `.env` и добавьте свои ключи:
```dotenv
YANDEX_IAM_TOKEN=your_yandex_token
JAMENDO_CLIENT_ID=your_jamendo_client_id
```

---

## ⚙Запуск

**CLI:**  
```bash
python ui/cli.py
```

**GUI (PyQt):**  
```bash
python ui/gui_qt.py
```

**Flask (Web):**  
```bash
python app.py
```

Открой [http://localhost:5000](http://localhost:5000) в браузере.

---

## Структура проекта

```
.
├── core/                  # Обработка изображений, видео, аудио
├── ui/                    # CLI и GUI интерфейсы
├── static/, templates/    # Фронтенд для Flask
├── input_*/ output/       # Медиафайлы
├── generated/             # Результаты генерации
├── app.py                 # Flask-приложение
├── main.py                # CLI-запуск
├── config.py              # Конфигурации (в .gitignore)
├── jamendo_api.py         # Jamendo API
├── image_generator.py     # Yandex Art API
└── .env                   # Переменные окружения (не коммитить!)
```

---

## Важно

- `.env` и `config.py` исключены из репозитория.
- Используй **Pillow < 10.0.0**, чтобы избежать ошибок с `moviepy`.

---

## Автор

Проект реализован **Александрой Новиковой**  
Контакт в Телеграм: "@an_alexandra_novikova"