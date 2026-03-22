import google.genai as genai
import os
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

response = client.models.generate_content(
    model="gemini-2.0-flash",
    contents="工場の安全確認AIとしてヘルメット未着用のリスクを一言で教えてください",
)
print(response.text)

