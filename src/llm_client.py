"""
Shared LLM client using OpenRouter (OpenAI-compatible API).
OpenRouter docs: https://openrouter.ai/docs
"""
import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_MODEL = os.getenv("OPENROUTER_MODEL", "meta-llama/llama-3.1-8b-instruct:free")

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=OPENROUTER_API_KEY,
)


def ask_llm(prompt: str, system: str = "You are a helpful assistant.") -> str:
    """Send a prompt to the configured OpenRouter model and return the text response."""
    if not OPENROUTER_API_KEY or OPENROUTER_API_KEY == "your_openrouter_api_key_here":
        raise ValueError(
            "OPENROUTER_API_KEY is missing or a placeholder. Set it in your .env file. "
            "Get one free at https://openrouter.ai/keys"
        )

    response = client.chat.completions.create(
        model=OPENROUTER_MODEL,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": prompt},
        ],
        temperature=0,
    )
    return response.choices[0].message.content.strip()
