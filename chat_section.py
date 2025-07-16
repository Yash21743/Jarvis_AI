from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QTextEdit, QLineEdit, QPushButton, QLabel, QFrame, QSizePolicy
from PyQt5.QtGui import QFont, QMovie, QColor, QIcon
from PyQt5.QtCore import Qt, QTimer, QSize
import os

# Paths
TempPath = os.path.join(os.getcwd(), "Frontend", "Files")
GraphicsPath = os.path.join(os.getcwd(), "Frontend", "Graphics", "YouTube - Jarvis Material For GUI").replace("\\", "/")


def GraphicsDirectoryPath(filename):
    return os.path.join(GraphicsPath, filename).replace("\\", "/")


class ChatSection(QWidget):
    def __init__(self):
        super(ChatSection, self).__init__()

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        # 📝 Chat Display
        self.chat_text_edit = QTextEdit()
        self.chat_text_edit.setReadOnly(True)
        self.chat_text_edit.setTextInteractionFlags(Qt.NoTextInteraction)
        self.chat_text_edit.setFrameStyle(QFrame.NoFrame)
        self.chat_text_edit.setFont(QFont("Arial", 13))
        self.chat_text_edit.setStyleSheet("color: white; background-color: black;")
        self.chat_text_edit.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        layout.addWidget(self.chat_text_edit, stretch=1)

        # 🔵 Orb
        self.gif_label = QLabel()
        movie = QMovie(GraphicsDirectoryPath("Jarvis.gif"))
        movie.setScaledSize(QSize(300, 200))
        self.gif_label.setAlignment(Qt.AlignRight | Qt.AlignBottom)
        self.gif_label.setMovie(movie)
        movie.start()
        layout.addWidget(self.gif_label, alignment=Qt.AlignRight)

        # 📢 Status label
        self.label = QLabel("")
        self.label.setStyleSheet("color: white; font-size: 16px;")
        self.label.setAlignment(Qt.AlignRight)
        layout.addWidget(self.label)

        # ⌨️ Input Field & Send Button
        input_layout = QHBoxLayout()
        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("Type here...")
        self.input_field.setStyleSheet("font-size: 15px; padding: 8px; color: white; background-color: black; border: 1px solid white;")
        self.input_field.returnPressed.connect(self.sendText)  # ✅ Press Enter to send
        input_layout.addWidget(self.input_field)

        self.send_button = QPushButton("Send")
        self.send_button.setStyleSheet("font-size: 14px; padding: 8px 15px; background-color: #2196F3; color: white; border-radius: 5px;")
        self.send_button.clicked.connect(self.sendText)
        input_layout.addWidget(self.send_button)

        layout.addLayout(input_layout)

        self.setLayout(layout)
        self.setStyleSheet("background-color: black;")

        # ⏱️ Timer setup
        self.shown_lines = set()
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.loadMessages)
        self.timer.timeout.connect(self.SpeechRecogText)
        self.timer.start(500)

    def loadMessages(self):
        response_path = os.path.join(TempPath, "Responses.data")
        if os.path.exists(response_path):
            with open(response_path, "r", encoding='utf-8') as file:
                lines = file.readlines()
            for line in lines:
                line = line.strip()
                if line and line not in self.shown_lines:
                    self.addMessage(line, "white")
                    self.shown_lines.add(line)

    def SpeechRecogText(self):
        status_path = os.path.join(TempPath, "Status.data")
        if os.path.exists(status_path):
            with open(status_path, "r", encoding='utf-8') as file:
                text = file.read()
            self.label.setText(text)

    def addMessage(self, message, color="white"):
        if message.startswith("Yash:"):
            self.chat_text_edit.setTextColor(QColor("#00BFFF"))  # Blue shade for user
        elif message.startswith("Jarvis:"):
            self.chat_text_edit.setTextColor(QColor("white"))    # White for Jarvis
        else:
            self.chat_text_edit.setTextColor(QColor(color))      # Default/fallback

        self.chat_text_edit.append(message)
        self.chat_text_edit.verticalScrollBar().setValue(self.chat_text_edit.verticalScrollBar().maximum())

    def sendText(self):
        query = self.input_field.text().strip()
        if query:
            try:
                from main import handle_input  # 🧠 Local import to avoid circular import
                handle_input(query)
            except Exception as e:
                print("Send Error:", e)
            self.input_field.clear()




