import os
from dotenv import load_dotenv

load_dotenv()

from google import genai  # google-genai SDK :contentReference[oaicite:1]{index=1}

API_KEY = os.getenv("GEMINI_API_KEY", "")
MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")

if not API_KEY:
    raise RuntimeError("Missing GEMINI_API_KEY in backend/.env")

client = genai.Client(api_key=API_KEY)

prompt = "Say 'Gemini is connected' and give one sentence about squats."

resp = client.models.generate_content(
    model=MODEL,
    contents=prompt,
)

print(resp.text)
