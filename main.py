import sys
import speech_recognition as sr
from PyQt5.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QPushButton, QLabel, QWidget)
from PyQt5.QtGui import QPixmap, QFont, QGuiApplication
from PyQt5.QtCore import Qt, QTimer

class AudioToTextApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Audio to Text Converter")
        self.resize(400, 400)
        self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnBottomHint)
        QTimer.singleShot(0, self.move_to_top_right)

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        self.label = QLabel("Press 'Start' to begin audio-to-text conversion", self)
        self.label.setFont(QFont("Arial", 12))
        self.label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.label)

        self.microphone_icon = QLabel(self)
        self.microphone_icon.setPixmap(QPixmap("mic_default.png").scaled(64, 64, Qt.KeepAspectRatio))
        self.microphone_icon.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.microphone_icon)

        self.start_button = QPushButton("Start", self)
        self.start_button.setStyleSheet("background-color: #4CAF50; color: white; font-size: 14px; padding: 10px;")
        self.start_button.clicked.connect(self.convert_audio_to_text)
        self.layout.addWidget(self.start_button)

        self.text_display = QLabel("Your transcribed text will appear here.", self)
        self.text_display.setFont(QFont("Arial", 10))
        self.text_display.setAlignment(Qt.AlignTop)
        self.text_display.setWordWrap(True)
        self.text_display.setStyleSheet("border: 1px solid #ccc; padding: 10px;")
        self.layout.addWidget(self.text_display)

        self.copy_button = QPushButton("Copy Text", self)
        self.copy_button.setStyleSheet("background-color: #2196F3; color: white; font-size: 14px; padding: 10px;")
        self.copy_button.clicked.connect(self.copy_text_to_clipboard)
        self.layout.addWidget(self.copy_button)

    def move_to_top_right(self):
        screen_geometry = QApplication.primaryScreen().availableGeometry()
        window_geometry = self.frameGeometry()

        x = screen_geometry.width() - window_geometry.width()
        y = 0

        self.move(x, y)

    def update_microphone_icon(self, state="default"):
        if state == "listening":
            self.microphone_icon.setPixmap(QPixmap("mic_listening.png").scaled(64, 64, Qt.KeepAspectRatio))
        elif state == "processing":
            self.microphone_icon.setPixmap(QPixmap("mic_processing.png").scaled(64, 64, Qt.KeepAspectRatio))
        else:
            self.microphone_icon.setPixmap(QPixmap("mic_default.png").scaled(64, 64, Qt.KeepAspectRatio))

    def copy_text_to_clipboard(self):
        """Copies the content of the text_display QLabel to the clipboard and resets it to placeholder text."""
        text = self.text_display.text()
        placeholder = "Your transcribed text will appear here."
        prefix = "Recognized Text: "

        if text and text != placeholder:
            if text.startswith(prefix):
                text = text[len(prefix):]

            clipboard = QGuiApplication.clipboard()
            clipboard.setText(text)
            self.text_display.setText(placeholder)
            self.label.setText("Text copied to clipboard and cleared!")
        else:
            self.label.setText("No text to copy!")

    def convert_audio_to_text(self):
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            self.start_button.setText("Recording...")
            self.start_button.setEnabled(False)
            self.label.setText("Listening... Speak now!")
            self.update_microphone_icon("listening")
            QApplication.processEvents()

            try:
                audio = recognizer.listen(source, timeout=10000)
                self.label.setText("Processing audio...")
                self.update_microphone_icon("processing")
                QApplication.processEvents()
                text = recognizer.recognize_google(audio)
                self.text_display.setText(f"Recognized Text: {text}")
                self.label.setText("Conversion complete.")
            except sr.UnknownValueError:
                self.text_display.setText("Could not understand audio.")
                self.label.setText("Error: Could not understand audio.")
            except sr.RequestError as e:
                self.text_display.setText(f"Error: {e}")
                self.label.setText("Error during processing.")
            finally:
                self.start_button.setText("Start")
                self.start_button.setEnabled(True)
                self.update_microphone_icon("default")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AudioToTextApp()
    window.show()
    sys.exit(app.exec_())


