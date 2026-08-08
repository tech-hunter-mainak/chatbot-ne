from app.config import SUPPORTED_LANGUAGES
from app.models.schemas import ChatResponse, SourceChunk
from app.services.retrieval_service import retrieval_service
from app.services.llm_service import llm_service


class RAGService:
    def answer(self, query: str, language: str) -> ChatResponse:
        if language not in SUPPORTED_LANGUAGES:
            raise ValueError(
                f"Unsupported language '{language}'. Supported: {list(SUPPORTED_LANGUAGES)}"
            )

        results = retrieval_service.retrieve(query, language)
        chunks = [text for text, _ in results]

        answer_text = llm_service.generate(query, chunks, language)

        return ChatResponse(
            answer=answer_text,
            language=language,
            sources=[SourceChunk(text=text, score=score) for text, score in results],
        )


rag_service = RAGService()
