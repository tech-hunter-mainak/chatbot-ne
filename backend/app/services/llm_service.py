import os
from typing import List

import httpx

from app.config import LLM_MODEL, GOOGLE_API_KEY


class LLMService:
    def __init__(self):
        self.model = LLM_MODEL
        self.google_api_key = GOOGLE_API_KEY

    async def generate(self, prompt: str) -> str:
        """Generate text from the configured LLM.

        If `GOOGLE_API_KEY` is configured we attempt to use the
        Google Generative API; otherwise this method raises an error
        instructing the user to configure their provider.
        """
        if self.google_api_key:
            # Use a simple HTTP call to Google Generative REST endpoint if available.
            # The exact API surface may differ; users should configure their keys.
            url = os.getenv("GOOGLE_GENERATIVE_URL", "https://generativelanguage.googleapis.com/v1beta2/models/{model}:generate")
            url = url.format(model=self.model)

            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.google_api_key}"
            }

            body = {
                "prompt": prompt,
                "maxOutputTokens": 512
            }

            async with httpx.AsyncClient(timeout=30) as client:
                resp = await client.post(url, json=body, headers=headers)
                resp.raise_for_status()
                data = resp.json()
                # best effort extraction
                if "candidates" in data:
                    return data["candidates"][0].get("content", "")
                return str(data)

        raise RuntimeError("No LLM provider configured. Set GOOGLE_API_KEY or implement an OpenAI adapter.")
