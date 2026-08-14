import requests

from app.config import OLLAMA_HOST, LLM_MODEL, NLLB_MODEL, SUPPORTED_LANGUAGES

SYSTEM_TEMPLATE = (
    "You are a helpful assistant answering questions about {lang_name} language and culture. "
    "Use ONLY the provided context to answer. If the context does not contain the answer, "
    "say you don't have that information instead of guessing. Reply in the same language "
    "the user asked in, unless they ask for a translation."
)


class TranslationService:
    _model = None
    _tokenizer = None
    _device = None

    @classmethod
    def _load_model(cls):
        if cls._model is None or cls._tokenizer is None:
            from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
            import torch

            cls._tokenizer = AutoTokenizer.from_pretrained(NLLB_MODEL, src_lang="ben_Beng", tgt_lang="asm_Beng")
            cls._model = AutoModelForSeq2SeqLM.from_pretrained(NLLB_MODEL)
            cls._device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
            cls._model.to(cls._device)

    @classmethod
    def translate_bengali_to_assamese(cls, text: str) -> str:
        cls._load_model()
        import torch

        inputs = cls._tokenizer(text, return_tensors="pt", truncation=True, max_length=1024).to(cls._device)
        forced_bos_id = cls._tokenizer.lang_code_to_id["<<asm_Beng>>"]
        with torch.no_grad():
            generated = cls._model.generate(**inputs, forced_bos_token_id=forced_bos_id, max_new_tokens=256)
        return cls._tokenizer.batch_decode(generated, skip_special_tokens=True)[0].strip()


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
        answer = response.json()["message"]["content"]

        if language == "asm":
            try:
                return TranslationService.translate_bengali_to_assamese(answer)
            except Exception:
                return answer

        return answer


llm_service = LLMService()
