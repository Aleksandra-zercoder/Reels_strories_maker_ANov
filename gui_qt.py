import sys
import os
import shutil
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QTextEdit, QPushButton, QFileDialog,
    QVBoxLayout, QHBoxLayout, QRadioButton, QButtonGroup, QMessageBox, QSpinBox
)
from PyQt5.QtGui import QDesktopServices
from PyQt5.QtCore import QUrl
from main import main as run_cli_main

TEMP_IMG_DIR = "input_images"
TEMP_AUDIO_DIR = "input_music"

class VideoMakerGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Vertical Video Maker")
        self.setGeometry(100, 100, 600, 560)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.setStyleSheet("""
            QWidget {
                background-color: #2b2b2b;
                color: #f0f0f0;
                font-family: 'Arial';
                font-size: 14px;
            }
            QLineEdit, QTextEdit, QSpinBox {
                background-color: #3c3f41;
                border: 1px solid #555;
                border-radius: 5px;
                padding: 5px;
                color: #f0f0f0;
            }
            QPushButton {
                background-color: #4CAF50;
                border: none;
                color: white;
                padding: 8px 16px;
                margin-top: 6px;
                font-size: 14px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QRadioButton {
                padding: 3px;
            }
            QLabel {
                margin-top: 8px;
            }
        """)

        # Выбор изображений
        layout.addWidget(QLabel("📸 Выберите изображения"))
        self.image_list = QLineEdit()
        self.image_list.setPlaceholderText("Файлы будут скопированы в input_images/")
        layout.addWidget(self.image_list)
        img_btn = QPushButton("Выбрать изображения")
        img_btn.clicked.connect(self.select_images)
        layout.addWidget(img_btn)

        # Выбор аудио
        layout.addWidget(QLabel("🎵 Выберите аудиофайл"))
        self.audio_path = QLineEdit()
        self.audio_path.setPlaceholderText("Файл будет скопирован в input_music/")
        layout.addWidget(self.audio_path)
        audio_btn = QPushButton("Выбрать аудио")
        audio_btn.clicked.connect(self.select_audio)
        layout.addWidget(audio_btn)

        # Логотип
        layout.addWidget(QLabel("🖼️ Логотип (опц.)"))
        self.logo_input = QLineEdit()
        layout.addWidget(self.logo_input)
        logo_btn = QPushButton("Выбрать логотип")
        logo_btn.clicked.connect(lambda: self.select_file(self.logo_input, ["*.png", "*.jpg", "*.jpeg"]))
        layout.addWidget(logo_btn)

        # Подпись
        layout.addWidget(QLabel("🔠 Подпись (опц.)"))
        self.caption_input = QTextEdit()
        self.caption_input.setFixedHeight(30)
        layout.addWidget(self.caption_input)

        # Режим подгонки
        layout.addWidget(QLabel("🎛️ Режим подгонки изображения"))
        self.mode_group = QButtonGroup(self)
        mode_layout = QHBoxLayout()
        for i, mode in enumerate(["center", "cover", "blur"]):
            btn = QRadioButton(mode)
            if i == 2:
                btn.setChecked(True)
            self.mode_group.addButton(btn)
            mode_layout.addWidget(btn)
        layout.addLayout(mode_layout)

        # Размер логотипа
        layout.addWidget(QLabel("📏 Размер логотипа (px)"))
        self.logo_size = QSpinBox()
        self.logo_size.setMinimum(10)
        self.logo_size.setMaximum(500)
        self.logo_size.setValue(100)
        layout.addWidget(self.logo_size)

        # Имя итогового файла
        layout.addWidget(QLabel("📝 Имя итогового видео (без .mp4)"))
        self.name_input = QLineEdit("my_video")
        layout.addWidget(self.name_input)

        # Кнопка генерации
        gen_btn = QPushButton("🚀 Сгенерировать видео")
        gen_btn.clicked.connect(self.generate_video)
        layout.addWidget(gen_btn)

        self.setLayout(layout)

    def select_images(self):
        files, _ = QFileDialog.getOpenFileNames(self, "Выберите изображения", "", "Images (*.png *.jpg *.jpeg)")
        if files:
            self.image_list.setText(", ".join(os.path.basename(f) for f in files))
            os.makedirs(TEMP_IMG_DIR, exist_ok=True)
            for f in os.listdir(TEMP_IMG_DIR):
                os.remove(os.path.join(TEMP_IMG_DIR, f))
            for path in files:
                shutil.copy(path, TEMP_IMG_DIR)

    def select_audio(self):
        file, _ = QFileDialog.getOpenFileName(self, "Выберите аудио", "", "Audio (*.mp3 *.wav)")
        if file:
            self.audio_path.setText(os.path.basename(file))
            os.makedirs(TEMP_AUDIO_DIR, exist_ok=True)
            for f in os.listdir(TEMP_AUDIO_DIR):
                os.remove(os.path.join(TEMP_AUDIO_DIR, f))
            shutil.copy(file, os.path.join(TEMP_AUDIO_DIR, os.path.basename(file)))

    def select_file(self, field, filters):
        file, _ = QFileDialog.getOpenFileName(self, "Выбрать файл", "", f"Files ({' '.join(filters)})")
        if file:
            field.setText(file)

    def generate_video(self):
        args = [
            "--images", TEMP_IMG_DIR,
            "--fit_mode", self.mode_group.checkedButton().text(),
            "--logo_size", str(self.logo_size.value()),
            "--name", self.name_input.text(),
            "--clean"
        ]

        if os.listdir(TEMP_AUDIO_DIR):
            args += ["--audio", os.path.join(TEMP_AUDIO_DIR, os.listdir(TEMP_AUDIO_DIR)[0])]
        if self.logo_input.text():
            args += ["--logo", self.logo_input.text()]
        if self.caption_input.toPlainText():
            args += ["--caption", self.caption_input.toPlainText()]

        try:
            sys.argv = ["main.py"] + args
            run_cli_main()
            output_file = f"output/{self.name_input.text()}.mp4"
            QDesktopServices.openUrl(QUrl.fromLocalFile(os.path.abspath(output_file)))
            QMessageBox.information(self, "Готово!", f"Видео сохранено: {output_file}")
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", str(e))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = VideoMakerGUI()
    window.show()
    sys.exit(app.exec_())
