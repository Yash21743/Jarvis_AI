
# 🤖 Jarvis AI - Python Desktop Assistant (Voice + GUI)

An intelligent voice + text assistant built with **Python** and **PyQt5** — inspired by Marvel’s Jarvis.  
Speak or type, and Jarvis listens, responds, automates, and talks back in a smooth, animated GUI.

---

## 🚀 Features

✅ Glowing Jarvis Orb Animation (GIF)  
✅ Voice & Text Input  
✅ Colored Chat Display  
✅ Auto Scroll Chat Panel  
✅ Text-to-Speech Responses  
✅ Basic Command Automation (open apps, play songs, etc.)  
✅ Image Generation Command Support  
✅ Single Window UI (No popup windows)

---

## 📁 Folder Structure

```
Jarvis AI/
├── Backend/
│   ├── Automation.py
│   ├── Chatbot.py
│   ├── RealtimeSearchEngine.py
│   ├── TextToSpeech.py
│   └── AnswerModifier.py (optional)
│
├── Frontend/
│   ├── GUI.py
│   ├── screens.py
│   ├── chat_section.py
│   ├── Files/
│   │   ├── Responses.data
│   │   ├── Status.data
│   │   ├── Mic.data
│   │   └── ImageGeneration.data
│   │
│   └── Graphics/
│       ├── Jarvis.gif
│       ├── Mic_on.png
│       ├── Mic_off.png
│       ├── Close.png
│       ├── Settings.png
│       ├── Home.png
│       ├── Chats.png
│       └── Maximize.png
│
├── Data/
│   └── (Optional models, logs, backups, etc.)
│
├── .venv/             # Python Virtual Environment
├── main.py            # Entry point
├── README.md
└── requirements.txt
```

---

## 📦 Requirements

Create a virtual environment and install:

```bash
pip install -r requirements.txt
```

### `requirements.txt` content:

```
PyQt5
SpeechRecognition
pyttsx3
gTTS
pygame
python-dotenv
```

> ⚠️ Note: You might also need to install `pyaudio`.  
Install via:

```bash
pip install pipwin
pipwin install pyaudio
```

---

## 🖥️ How to Run

```bash
python main.py
```

---

## 💬 Supported Commands

```bash
hello
what is AI?
open notepad
play music
generate image of tony stark
open whatsapp
```

You can customize responses in `Chatbot.py`.

---

## 🎨 Chat Display

| Speaker | Color |
|---------|--------|
| You (Yash) | 🟦 Blue |
| Jarvis     | ⚪ White |

---

## 📸 Screenshots

| Home (Orb) | Chat Panel |
|------------|-------------|
| ![Orb](./Frontend/Graphics/Jarvis.gif) | Auto scroll, color-coded |

---

## 👨‍💻 Developer Info

**👤 Yash (Y@shuu)**  
📍 India  
💬 Python Automation & AI Projects  
🔗 [LinkedIn](https://www.linkedin.com/in/your-profile)

---

## ⚠️ Notes

- Add your `.env` file (optional) for `Assistantname` or API keys
- Keep `Jarvis.gif` inside `/Frontend/Graphics`
- Don't delete `.data` files from `/Frontend/Files/`

---

## 📌 To Upload on GitHub

1. Delete `.venv` folder (too heavy)
2. Zip folder or upload via Git
3. Include:
   - All `.py` files
   - `/Frontend/Graphics/`
   - `/Frontend/Files/`
   - `requirements.txt`
   - This `README.md`

---

## ✅ To Upload on LinkedIn

1. Create a new post:  
   _"🚀 Just built my own Jarvis AI..."_
2. Attach screenshots or a screen-recording
3. Add GitHub repo link
4. Tag #Python #AI #Jarvis #Portfolio

---

Made with 💙 by Yash — because Iron Man was busy 😎
