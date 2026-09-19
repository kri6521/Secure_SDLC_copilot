import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

class GroqLLM:
    def __init__(self):
        self.api_key = os.getenv("GROQ_API_KEY")
        self.model = os.getenv("GROQ_MODEL", "openai/gpt-oss-120b")
        if not self.api_key:
            raise RuntimeError("GROQ_API_KEY is not configured. Copy .env.example to .env.")
        self.client = Groq(api_key=self.api_key)

    def ask(self, system: str, user: str) -> str:
        response = self.client.chat.completions.create(
            model=self.model,
            temperature=0.1,
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
        )
        return response.choices[0].message.content or ""
