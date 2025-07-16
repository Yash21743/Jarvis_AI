from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from PyQt5.QtGui import QMovie, QIcon
from PyQt5.QtCore import Qt, QSize
from Frontend.chat_section import ChatSection
import os


current_dir = os.getcwd()
GraphicsDirPath = os.path.join(current_dir, "Frontend", "Graphics", "YouTube - Jarvis Material For GUI").replace("\\", "/")


def GraphicsDirectoryPath(Filename):
    return rf"{GraphicsDirPath}/{Filename}"

class InitialScreen(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)

        # 🔵 Jarvis Glowing Orb (BIG)
        self.gif_label = QLabel()
        self.gif_label.setFixedSize(500, 500)
        self.gif_label.setStyleSheet("background-color: transparent; border-radius: 250px;")

        movie = QMovie(GraphicsDirectoryPath("Jarvis.gif"))
        movie.setScaledSize(QSize(500, 500))
        self.gif_label.setMovie(movie)
        movie.start()
        layout.addWidget(self.gif_label, alignment=Qt.AlignCenter)

        # 📝 Translating Text
        self.status_label = QLabel("Translating...")
        self.status_label.setStyleSheet("color: white; font-size: 20px;")
        self.status_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.status_label)

        # 🎤 Mic Toggle Button
        self.mic_button = QPushButton()
        self.mic_on_icon = QIcon(GraphicsDirectoryPath("Mic_on.png"))
        self.mic_off_icon = QIcon(GraphicsDirectoryPath("Mic_off.png"))
        self.mic_on = True  # default state

        self.mic_button.setIcon(self.mic_on_icon)
        self.mic_button.setIconSize(QSize(32, 32))
        self.mic_button.setFixedSize(65, 65)
        self.mic_button.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                border-radius: 32px;
                border: none;
            }
            QPushButton:hover {
                background-color: #1976D2;
            }
        """)
        self.mic_button.clicked.connect(self.listen_and_send)
        layout.addWidget(self.mic_button, alignment=Qt.AlignCenter)

        self.setLayout(layout)
        self.setStyleSheet("background-color: black;")

    def toggleMic(self):
        if self.mic_on:
            self.mic_button.setIcon(self.mic_off_icon)
            self.status_label.setText("Mic Off")
            self.mic_on = False
        else:
            self.mic_button.setIcon(self.mic_on_icon)
            self.status_label.setText("Translating...")
            self.mic_on = True

    def listen_and_send(self):
        try:
            import speech_recognition as sr
            from Backend.TextToSpeech import TextToSpeech
            from Backend.Chatbot import ChatBot
            from Backend.Automation import Automation
            import asyncio

            recognizer = sr.Recognizer()
            with sr.Microphone() as source:
                self.status_label.setText("Listening...")
                print("🎤 Listening...")
                audio = recognizer.listen(source, timeout=5)

            query = recognizer.recognize_google(audio)
            print("You said:", query)

            # Prepare messages
            user_msg = f"Yash: {query}"
            bot_msg = f"Jarvis: {ChatBot(query)}"

            # Write to Responses.data
            responses_path = os.path.join(os.getcwd(), "Frontend", "Files", "Responses.data")
            with open(responses_path, "a", encoding="utf-8") as file:
                file.write(user_msg + "\\n")
                file.write(bot_msg + "\\n")

            # Speak reply
            TextToSpeech(bot_msg)

            # Run automation
            asyncio.run(Automation([query.lower()]))

            self.status_label.setText("Translating...")

        except Exception as e:
            print("Mic error:", e)
            self.status_label.setText("Mic Error")
        


from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QTextEdit
from PyQt5.QtGui import QFont, QColor, QMovie
from PyQt5.QtCore import Qt, QSize, QTimer
import os

current_dir = os.getcwd()
TempDirPath = rf"{current_dir}\\Frontend\\Files"
GraphicsDirPath = os.path.join(current_dir, "Frontend", "Graphics", "YouTube - Jarvis Material For GUI").replace("\\", "/")
old_chat_message = ""

def GraphicsDirectoryPath(Filename):
    return rf"{GraphicsDirPath}\\{Filename}"

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QTextEdit
from PyQt5.QtGui import QFont, QColor, QMovie
from PyQt5.QtCore import Qt, QSize, QTimer
import os

current_dir = os.getcwd()
TempDirPath = rf"{current_dir}\\Frontend\\Files"
GraphicsDirPath = os.path.join(current_dir, "Frontend", "Graphics", "YouTube - Jarvis Material For GUI").replace('\\\\', '/')

def GraphicsDirectoryPath(Filename):
    return rf"{GraphicsDirPath}/{Filename}"

class MessageScreen(QWidget):
    def __init__(self):
        super().__init__()

        self.setStyleSheet("background-color: black;")
        self.layout = QVBoxLayout(self)

        self.last_content = ""
        self.layout.setContentsMargins(20, 20, 20, 100)
        self.layout.setSpacing(10)

        # Chat display box
        self.chat_text_edit = QTextEdit()
        self.chat_text_edit.setReadOnly(True)
        self.chat_text_edit.setTextInteractionFlags(Qt.NoTextInteraction)
        self.chat_text_edit.setStyleSheet("color: white; background-color: transparent; border: none;")
        font = QFont()
        font.setPointSize(14)
        self.chat_text_edit.setFont(font)
        self.layout.addWidget(self.chat_text_edit)

        # Orb GIF bottom-right
        self.gif_label = QLabel(self)
        self.gif_label.setFixedSize(180, 180)
        self.gif_label.setStyleSheet("background-color: transparent;")
        self.gif_label.setAttribute(Qt.WA_TranslucentBackground)
        movie = QMovie(GraphicsDirectoryPath("Jarvis.gif"))
        movie.setScaledSize(QSize(180, 180))
        self.gif_label.setMovie(movie)
        movie.start()

        # Translating label
        self.status_label = QLabel("Translating...", self)
        self.status_label.setStyleSheet("color: white; font-size: 14px;")

        # Resize event to keep them in corner
        self.resizeEvent = self.positionOverlayWidgets

        # Track full content
        self.last_content = ""

        # Auto update
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.loadMessages)
        self.timer.timeout.connect(self.updateStatus)
        self.timer.start(500)

    def loadMessages(self):
        try:
            response_path = rf"{TempDirPath}\\Responses.data"
            if os.path.exists(response_path):
                with open(response_path, "r", encoding='utf-8') as file:
                    content = file.read()

                if content.strip() != self.last_content:
                    self.chat_text_edit.setTextColor(QColor("white"))
                    self.chat_text_edit.setPlainText(content.strip())
                    self.last_content = content.strip()
        except Exception as e:
            print("Error loading messages:", e)

    def updateStatus(self):
        try:
            with open(rf"{TempDirPath}\\Status.data", "r", encoding='utf-8') as file:
                messages = file.read()
            self.status_label.setText(messages)
        except:
            self.status_label.setText("")

    def positionOverlayWidgets(self, event):
        self.gif_label.move(self.width() - 200, self.height() - 200)
        self.status_label.move(self.width() - 200, self.height() - 40)