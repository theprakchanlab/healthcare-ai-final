from dotenv import load_dotenv
import os

load_dotenv()

key = os.getenv("OPENAI_API_KEY")

if key:
    print("✅ API Key Loaded")
    print(key[:15] + "...")
else:
    print("❌ API Key NOT Found")