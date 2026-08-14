from typing import Optional

from app.config import SUPPORTED_LANGUAGES
from app.models.schemas import ChatResponse, SourceChunk
from app.services.retrieval_service import retrieval_service
from app.services.llm_service import llm_service
from app.services.math_service import math_service
from app.services.session_service import session_service


class RAGService:
    def answer(self, query: str, language: str, session_id: Optional[str] = None) -> ChatResponse:
        if language not in SUPPORTED_LANGUAGES:
            raise ValueError(
                f"Unsupported language '{language}'. Supported: {list(SUPPORTED_LANGUAGES)}"
            )

        # Quick path: if the user asked a simple arithmetic question, evaluate locally
        math_result = math_service.try_evaluate(query)
        if math_result is not None:
            resp = ChatResponse(answer=math_result, language=language, sources=[])
            if session_id:
                try:
                    session_service.append(session_id, {"user": query, "bot": resp.answer})
                except Exception:
                    pass
            return resp

        results = retrieval_service.retrieve(query, language)
        chunks = [text for text, _ in results]

        answer_text = llm_service.generate(query, chunks, language)

        resp = ChatResponse(
            answer=answer_text,
            language=language,
            sources=[SourceChunk(text=text, score=score) for text, score in results],
        )

        if session_id:
            try:
                session_service.append(session_id, {"user": query, "bot": resp.answer})
            except Exception:
                pass

        return resp


rag_service = RAGService()
