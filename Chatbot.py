from groq import Groq  # Importing the groq library to use its  API.
from json import load, dump 
import datetime
from dotenv import dotenv_values
import os
import webbrowser

env_vars = dotenv_values(".env")

Username = env_vars.get("Username")
Assistantname = env_vars.get("Assistantname")
GroqAPIKey = env_vars.get("GroqAPIKey")

client = Groq(api_key=GroqAPIKey)

messages = []

# System = f"""Hello, I am {Username}, You are a very accurate and advanced AI chatbot named {Assistantname} which also has real-time up-to-date information from the internet.
# *** Do not tell time until I ask, do not talk too much, just answer the question.***
# *** Reply in only English, even if the question is in Hindi, reply in English.***
# *** Do not provide notes in the output, just answer the question and never mention your training data. ***
# """
# System = f"""You are an intelligent assistant named {Assistantname}.
# Always reply helpfully and respectfully.
# ❌ Do not prefix replies with your name like 'Jarvis:' or 'Assistant:'.
# ✅ Just say the response directly."""
# System = f"""You are an intelligent assistant named {Assistantname}.
# - Reply respectfully and helpfully.
# - ❌ Do not prefix replies with your name like 'Jarvis:', 'Assistant:', or 'AI:'.
# - ✅ Just say the response directly.
# - Do not introduce yourself in every answer.
# - Do not repeat 'I am Jarvis' or similar lines unless asked.
# """
System = f"""
You are a respectful AI assistant named {Assistantname}.
NEVER prefix your replies with 'Jarvis:', 'Assistant:', or 'AI:'.
NEVER say 'Jarvis:' at the start of any sentence.
If user says 'hello', you just say 'Hello!', not 'Jarvis: Hello!'
Give direct, short, polite answers. Just answer. No introductions.
"""

SystemChatBot = [{"role": "system", "content": System}]

try:
    with open(r"Data\ChatLog.json", "r") as f:
        messages = load(f)
except FileNotFoundError:
    with open(r"Data\ChatLog.json", "w") as f:
        dump([], f)

def RealtimeInformation():
    current_date_time = datetime.datetime.now()
    day = current_date_time.strftime("%A")
    date = current_date_time.strftime("%d") 
    month = current_date_time.strftime("%B") 
    year = current_date_time.strftime("%Y") 
    hour = current_date_time.strftime("%H") 
    minute = current_date_time.strftime("%M") 
    second = current_date_time.strftime("%S")   

    data = f"Please use this real-time information if needed,\n"
    data += f"Day: {day}\nDate: {date}\n Month:{month}\nYear: {year}\n"
    data += f"Time: {hour} hours: {minute} minutes :{second} seconds.\n"
    return data

# def AnswerModifier(Answer):
#     lines = Answer.split('\n')
#     non_empty_lines = [line for line in lines if line.strip()]
#     modified_answer = '\n'.join(non_empty_lines)
#     return modified_answer
# def AnswerModifier(Answer: str) -> str:
#     lines = Answer.split('\n')
#     cleaned = []

#     for line in lines:
#         line = line.strip()

#         # Remove prefixes like Jarvis:, Assistant:, etc.
#         for prefix in ["jarvis:", "Jarvis:", "assistant:", "Assistant:", "AI:", "ai:"]:
#             if line.startswith(prefix):
#                 line = line[len(prefix):].strip()

#         if line:
#             cleaned.append(line)

#     return '\n'.join(cleaned)
def AnswerModifier(Answer: str) -> str:
    """
    Clean and simplify AI response:
    - Remove prefixes like 'Jarvis:', 'Assistant:', 'AI:'
    - Remove extra blank lines and spaces
    - Return clean, readable answer
    """
    lines = Answer.split('\n')
    cleaned = []

    for line in lines:
        line = line.strip()

        # Remove unwanted prefixes
        unwanted_prefixes = ["jarvis:", "assistant:", "ai:"]
        for prefix in unwanted_prefixes:
            if line.lower().startswith(prefix):
                line = line[len(prefix):].strip()

        if line:  # only add non-empty lines
            cleaned.append(line)

    return '\n'.join(cleaned)


def ChatBot(Query):
    """ This function sends the user's query to the chatbot and returns the AI's response."""

    QueryLower = Query.lower()

    # ✅ Smart Open/Play Handler
    if any(x in QueryLower for x in ["open", "play", "launch", "start"]):
        app_name = Query.replace("open", "").replace("play", "").replace("launch", "").replace("start", "").strip()

        # Website shortcuts
        if "youtube" in QueryLower:
            webbrowser.open("https://www.youtube.com/")
        elif "instagram" in QueryLower:
            webbrowser.open("https://www.instagram.com/")
        elif "chrome" in QueryLower:
            os.system("start chrome")
        # System apps
        elif "notepad" in QueryLower:
            os.system("notepad")
        elif "calculator" in QueryLower:
            os.system("calc")
        elif "paint" in QueryLower:
            os.system("mspaint")
        else:
            try:
                os.system(app_name)
            except:
                return f"Sorry sir, I couldn't open {app_name}"

        return f"Sure sir, opening {app_name.title()} for you "

    # ✅ Otherwise, use AI Model
    try:
        with open(r"Data\ChatLog.json", "r") as f:
            messages = load(f)

        messages.append({"role": "user", "content": f"{Query}"})

        completion = client.chat.completions.create(
            model="llama3-70b-8192",
            messages=SystemChatBot + [{"role": "system", "content": RealtimeInformation()}] + messages,
            max_tokens=1024,
            temperature=0.7,
            top_p=1,
            stream=True,
            stop=None
        )

        Answer = ""
        for chunk in completion:
            if chunk.choices[0].delta.content:
                Answer += chunk.choices[0].delta.content

        Answer = Answer.replace("<\s>", "")
        messages.append({"role": "assistant", "content": Answer})

        with open(r"Data\ChatLog.json", "w") as f:
            dump(messages, f, indent=4)

        print("💡 Before Modifier:", Answer)
        print("✅ After Modifier:", AnswerModifier(Answer))


        return AnswerModifier(Answer=Answer)

    except Exception as e:
        print(f"Error: {e}")
        with open(r"Data\ChatLog.json", "w") as f:
            dump([], f, indent=4)
        return ChatBot(Query)    

if __name__ == "__main__":
    while True:
        user_input = input("Enter Your Questions: ")
        print(ChatBot(user_input))
