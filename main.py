import sys
import os
import speech_recognition as sr
from PyQt5.QtWidgets import QApplication
from Frontend.GUI import MainWindow
from Backend.TextToSpeech import TextToSpeech
from Backend.Chatbot import ChatBot
from Backend.Automation import Automation
import asyncio

# ✅ File path
response_path = os.path.join(os.getcwd(), "Frontend", "Files", "Responses.data")

# 🎤 Speech recognizer
recognizer = sr.Recognizer()

# ✅ Save and Respond
def handle_input(text):
    if not text.strip():
        return

    user_message = f"Yash: {text.strip()}"
    ai_reply = f"Jarvis: {ChatBot(text)}"

    # 💬 Save to chat screen file
    with open(response_path, "a", encoding="utf-8") as file:
        file.write(user_message + "\n")
        file.write(ai_reply + "\n")

    # 🗣 Speak the reply
    TextToSpeech(ai_reply)

    # ⚙️ Automation
    try:
        asyncio.run(Automation([text.lower()]))
    except Exception as e:
        print("Automation error:", e)

# 🧠 Main
if __name__ == "__main__":
    app = QApplication(sys.argv)
    gui = MainWindow()
    gui.show()
    sys.exit(app.exec_())
