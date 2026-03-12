import requests
import os
from dotenv import load_dotenv

load_dotenv()
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

url = f"https://generativelanguage.googleapis.com/v1beta/models?key={GEMINI_API_KEY}"
response = requests.get(url)

if response.status_code == 200:
    models = response.json().get("models", [])
    for model in models:
        if "image" in model["name"].lower() or "predict" in model["supportedGenerationMethods"]:
            print(f"Name: {model['name']} | Methods: {model['supportedGenerationMethods']}")
else:
    print(f"Error: {response.status_code}")
    print(response.text)
