
import os

from dotenv import load_dotenv
from google import genai

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY not found in .env")

client = genai.Client(api_key=api_key)

print("Checking available Gemini models...\n")

for model in client.models.list():
    actions = getattr(model, "supported_actions", [])
    
    if "generateContent" in actions:
        print("Model:", model.name)
        print("Supported actions:", actions)
        print("--------------------------")
