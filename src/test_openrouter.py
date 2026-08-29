"""
Quick test to confirm your OpenRouter API key works.

Run:
    python src/test_openrouter.py
"""
import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

api_key = os.getenv("OPENROUTER_API_KEY")
model = os.getenv("OPENROUTER_MODEL", "meta-llama/llama-3.1-8b-instruct:free")

if not api_key:
    raise SystemExit("OPENROUTER_API_KEY not found in .env — add it and try again.")

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key,
)

response = client.chat.completions.create(
    model=model,
    messages=[
        {"role": "user", "content": "Reply with exactly: OpenRouter connection successful."}
    ],
)

print(response.choices[0].message.content)
