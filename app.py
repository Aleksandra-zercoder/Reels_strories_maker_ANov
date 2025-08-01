from flask import Flask, render_template, request, redirect, send_from_directory, jsonify, url_for
from werkzeug.utils import secure_filename
import os
import uuid
import sys

from jamendo_api import search_music, download_music_file
from image_generator import generate_image
from main import main as run_cli_main

app = Flask(__name__)
UPLOAD_FOLDER = "static/uploads"
GENERATED_FOLDER = "static/generated"
OUTPUT_FOLDER = "output"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(GENERATED_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # AJAX-запрос генерации AI-изображений
        if request.headers.get("X-Requested-With") == "XMLHttpRequest" and request.form.get("generate_ai") == "true":
            prompt1 = request.form.get("prompt1", "").strip()
            prompt2 = request.form.get("prompt2", "").strip()
            generated_images = []

            if prompt1:
                img1 = generate_image(prompt1, output_path=os.path.join(GENERATED_FOLDER, "img1.jpg"))
                generated_images.append(os.path.basename(img1))
            if prompt2:
                img2 = generate_image(prompt2, output_path=os.path.join(GENERATED_FOLDER, "img2.jpg"))
                generated_images.append(os.path.basename(img2))

            return jsonify({"images": generated_images})

        # --- Генерация видео ---
        session_id = str(uuid.uuid4())[:8]
        temp_img_dir = os.path.join(UPLOAD_FOLDER, session_id, "images")
        temp_audio_dir = os.path.join(UPLOAD_FOLDER, session_id, "audio")
        os.makedirs(temp_img_dir, exist_ok=True)
        os.makedirs(temp_audio_dir, exist_ok=True)

        # Загружаем изображения
        for f in request.files.getlist("images"):
            if f and f.filename:
                f.save(os.path.join(temp_img_dir, secure_filename(f.filename)))

        # Добавляем выбранные AI-изображения
        for img_name in request.form.getlist("use_generated[]"):
            src_path = os.path.join(GENERATED_FOLDER, img_name)
            dst_path = os.path.join(temp_img_dir, img_name)
            if os.path.exists(src_path):
                with open(src_path, "rb") as src, open(dst_path, "wb") as dst:
                    dst.write(src.read())

        # Добавляем видео
        video_file = request.files.get("video")
        if video_file and video_file.filename:
            video_path = os.path.join(temp_img_dir, secure_filename(video_file.filename))
            video_file.save(video_path)

        # Логотип
        logo_path = ""
        logo_file = request.files.get("logo")
        if logo_file and logo_file.filename:
            temp_logo_dir = os.path.join(UPLOAD_FOLDER, session_id, "logo")
            os.makedirs(temp_logo_dir, exist_ok=True)
            logo_path = os.path.join(temp_logo_dir, secure_filename(logo_file.filename))
            logo_file.save(logo_path)

        # Аудио
        audio_path = ""
        audio_file = request.files.get("audio")
        if audio_file and audio_file.filename:
            audio_path = os.path.join(temp_audio_dir, secure_filename(audio_file.filename))
            audio_file.save(audio_path)
        else:
            selected_audio_url = request.form.get("selected_music_url")
            if selected_audio_url:
                audio_path = os.path.join(temp_audio_dir, "selected_track.mp3")
                download_music_file(selected_audio_url, audio_path)

        # Прочие настройки
        caption = request.form.get("caption", "")
        fit_mode = request.form.get("fit_mode", "cover")
        logo_size = request.form.get("logo_size", "100")
        name = request.form.get("name", f"video_{session_id}")

        # Аргументы для генерации видео
        args = [
            "--images", temp_img_dir,
            "--fit_mode", fit_mode,
            "--name", name,
            "--logo_size", logo_size,
        ]
        if caption:
            args += ["--caption", caption]
        if logo_path:
            args += ["--logo", logo_path]
        if audio_path:
            args += ["--audio", audio_path]

        sys.argv = ["main.py"] + args
        run_cli_main()

        return redirect(url_for("preview_video", filename=f"{name}.mp4"))

    return render_template("index.html")


@app.route("/search_music")
def search_music_route():
    query = request.args.get("q", "")
    if not query:
        return jsonify([])
    try:
        return jsonify(search_music(query))
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/preview/<filename>")
def preview_video(filename):
    return f"""
    <!DOCTYPE html>
    <html lang="ru">
    <head>
        <meta charset="UTF-8">
        <title>Ваше видео готово!</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
        <style>
            body {{
                background-color: #121212;
                color: white;
                text-align: center;
                padding: 2rem;
            }}
            video {{
                max-width: 100%;
                border-radius: 1rem;
                margin-bottom: 2rem;
            }}
        </style>
    </head>
    <body>
        <h2>🎉 Ваше видео готово!</h2>
        <video controls src="/output/{filename}"></video>
        <br>
        <a href="/output/{filename}" download class="btn btn-success btn-lg">📥 Скачать видео</a>
        <a href="/" class="btn btn-outline-light btn-lg ms-2">⬅ Вернуться</a>
    </body>
    </html>
    """


@app.route("/output/<filename>")
def download_file(filename):
    return send_from_directory("output", filename, as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True)
