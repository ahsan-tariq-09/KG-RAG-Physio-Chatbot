import os
from dotenv import load_dotenv
load_dotenv()

from google import genai

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

for m in client.models.list():
    # Print name + supported methods (if available)
    print(m.name)
    if hasattr(m, "supported_actions") and m.supported_actions:
        print("  supported:", m.supported_actions)
