import requests

from app.config import OLLAMA_HOST, LLM_MODEL, SUPPORTED_LANGUAGES

SYSTEM_TEMPLATE = (
    "You are a helpful assistant answering questions about {lang_name} language and culture. "
    "Use ONLY the provided context to answer. If the context does not contain the answer, "
    "say you don't have that information instead of guessing. Reply in the same language "
    "the user asked in, unless they ask for a translation."
)


class LLMService:
    """Talks to a local Ollama server — free, open-source, no API key."""

    def generate(self, query: str, context_chunks: list[str], language: str) -> str:
        lang_name = SUPPORTED_LANGUAGES.get(language, language)
        context = "\n\n".join(context_chunks) if context_chunks else "No relevant context found."

        system_prompt = SYSTEM_TEMPLATE.format(lang_name=lang_name)
        user_prompt = f"Context:\n{context}\n\nQuestion: {query}"

        response = requests.post(
            f"{OLLAMA_HOST}/api/chat",
            json={
                "model": LLM_MODEL,
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                "stream": False,
            },
            timeout=120,
        )
        response.raise_for_status()
        return response.json()["message"]["content"]


llm_service = LLMService()
