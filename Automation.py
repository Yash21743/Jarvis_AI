# Import required libraries
from AppOpener import close, open as appopen
from webbrowser import open as webopen
from pywhatkit import search, playonyt
from dotenv import dotenv_values
from bs4 import BeautifulSoup
from rich import print
from groq import Client, Groq
import webbrowser
import subprocess
import requests
import keyboard
import asyncio
import os

# Load environment variables
env_vars = dotenv_values(".env")
GroqAPIKey = env_vars.get("GroqAPIKey")

# Groq Client (if needed for content generation)
client = Groq(api_key=GroqAPIKey)

# User-Agent for search
useragent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36'

# HTML parsing classes (not always needed now)
classes = []

# Content creation system context
SystemChatBot = [{"role": "system", "content": f"Hello, I am {os.environ['Username']}, You're a content writer. You have to write content like letter"}]

messages = []

# ✅ Google Search
def GoogleSearch(Topic):
    search(Topic)
    return True

# ✅ YouTube Search
def YouTubeSearch(Topic):
    Url4Search = f"https://www.youtube.com/results?search_query={Topic}"
    webbrowser.open(Url4Search)
    return True

# ✅ Play YouTube video directly
def PlayYoutube(query):
    playonyt(query)
    return True

# ✅ Content Writer + Save to File
def Content(Topic):
    def OpenNotepad(File):
        subprocess.Popen(["notepad.exe", File])

    def ContentWriterAI(prompt):
        messages.append({"role": "user", "content": f"{prompt}"})
        completion = client.chat.completions.create(
            model="mistral-saba-24b",
            messages=SystemChatBot + messages,
            max_tokens=2048,
            temperature=0.7,
            top_p=1,
            stream=True
        )
        Answer = ""
        for chunk in completion:
            if chunk.choices[0].delta.content:
                Answer += chunk.choices[0].delta.content
        messages.append({"role": "assistant", "content": Answer})
        return Answer.replace("</s>", "")

    Topic = Topic.replace("content", "").strip()
    result = ContentWriterAI(Topic)
    filepath = rf"Data\{Topic.lower().replace(' ', '')}.txt"
    with open(filepath, "w", encoding="utf-8") as file:
        file.write(result)
    OpenNotepad(filepath)
    return True

# ✅ App opener
def OpenApp(app, sess=requests.session()):
    try:
        appopen(app, match_closest=True, output=True, throw_error=True)
        return True
    except:
        def search_google(query):
            url = f"https://www.google.com/search?q={query}"
            headers = {"User-Agent": useragent}
            res = sess.get(url, headers=headers)
            return res.text if res.status_code == 200 else None

        def extract_links(html):
            soup = BeautifulSoup(html, 'html.parser')
            links = soup.find_all('a')
            return [link.get('href') for link in links if link.get('href')]

        html = search_google(app)
        if html:
            links = extract_links(html)
            if links:
                webopen(f"https://www.google.com{links[0]}")
        return True

# ✅ App closer
def CloseApp(app):
    if "chrome" in app:
        return False
    try:
        close(app, match_closest=True, output=True, throw_error=True)
        return True
    except:
        return False

# ✅ System control (mute, volume etc.)
def System(command):
    if command == "mute":
        keyboard.press_and_release("volume mute")
    elif command == "unmute":
        keyboard.press_and_release("volume mute")
    elif command == "volume up":
        keyboard.press_and_release("volume up")
    elif command == "volume down":
        keyboard.press_and_release("volume down")
    return True

# ✅ Translate user commands and match functions
async def TranslateAndExecute(commands: list[str]):
    funcs = []

    for cmd in commands:
        cmd = cmd.lower().strip()

        if cmd.startswith("open "):
            funcs.append(asyncio.to_thread(OpenApp, cmd[5:].strip()))

        elif cmd.startswith("close "):
            funcs.append(asyncio.to_thread(CloseApp, cmd[6:].strip()))

        elif cmd.startswith("play "):
            funcs.append(asyncio.to_thread(PlayYoutube, cmd[5:].strip()))

        elif cmd.startswith("content "):
            funcs.append(asyncio.to_thread(Content, cmd[8:].strip()))

        elif cmd.startswith("google search "):
            funcs.append(asyncio.to_thread(GoogleSearch, cmd[14:].strip()))

        elif cmd.startswith("youtube search "):
            funcs.append(asyncio.to_thread(YouTubeSearch, cmd[15:].strip()))

        elif cmd.startswith("system "):
            funcs.append(asyncio.to_thread(System, cmd[7:].strip()))

        else:
            print(f"[yellow]⚠️ No FunctionFound.For → {cmd}")

    results = await asyncio.gather(*funcs)
    for result in results:
        yield result

# ✅ Entry: call this from main.py
async def Automation(commands: list[str]):
    async for _ in TranslateAndExecute(commands):
        pass
    return True

# 🧪 Test
if __name__ == "__main__":
    asyncio.run(Automation([ ]))

