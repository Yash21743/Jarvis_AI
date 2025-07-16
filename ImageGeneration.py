import asyncio
from random import randint
from PIL import Image
import requests
from dotenv import get_key
import os
from time import sleep

# ✅ HuggingFace API setup
API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"
headers = {"Authorization": f"Bearer {get_key('.env', 'HuggingFaceAPIKey')}"}

# ✅ Image output directory
folder_path = r"Data"

# 🔧 Replace spaces with underscores for filenames
def format_filename(prompt):
    return prompt.replace(" ", "_").strip()

# ✅ Query HuggingFace API (runs in background thread)
async def query(payload):
    response = await asyncio.to_thread(requests.post, API_URL, headers=headers, json=payload)
    return response.content

# ✅ Generate 4 images from prompt
async def generate_image(prompt: str):
    prompt = prompt.strip()
    tasks = []

    for _ in range(4):
        payload = {
            "inputs": f"{prompt}, 4k, ultra detailed, realistic, seed={randint(1, 999999)}"
        }
        tasks.append(asyncio.create_task(query(payload)))

    results = await asyncio.gather(*tasks)

    # Save images
    for i, img_data in enumerate(results):
        file_name = os.path.join(folder_path, f"{format_filename(prompt)}_{i+1}.jpg")
        with open(file_name, "wb") as f:
            f.write(img_data)

# ✅ Display generated images
def open_images(prompt):
    prompt = format_filename(prompt)
    for i in range(1, 5):
        img_path = os.path.join(folder_path, f"{prompt}_{i}.jpg")
        try:
            img = Image.open(img_path)
            print(f"Opening: {img_path}")
            img.show()
            sleep(1)  # wait before opening next
        except:
            print(f"❌ Couldn't open {img_path}")

# ✅ Wrapper: Generate + Show
def GenerateImages(prompt: str):
    asyncio.run(generate_image(prompt))
    open_images(prompt)

# ✅ Continuous monitor loop
while True:
    try:
        with open(r"Frontend\Files\ImageGeneration.data", "r") as f:
            data = f.read().strip()

        if "," not in data:
            sleep(1)
            continue

        prompt, status = data.split(",")

        if status.strip() == "True":
            print(f"🧠 Generating images for prompt: {prompt}")
            GenerateImages(prompt)

            # ✅ Reset status after processing
            with open(r"Frontend\Files\ImageGeneration.data", "w") as f:
                f.write("False,False")

            break

        else:
            sleep(1)

    except Exception as e:
        print("❌ Error:", e)
        sleep(1)
