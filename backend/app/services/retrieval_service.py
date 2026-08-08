from app.config import CHUNK_SIZE, CHUNK_OVERLAP, TOP_K
from app.services.embedding_service import embedding_service
from app.vectorstore.faiss_manager import FaissManager


def chunk_text(text: str, size: int = CHUNK_SIZE, overlap: int = CHUNK_OVERLAP) -> list[str]:
    text = " ".join(text.split())  # collapse whitespace
    chunks = []
    start = 0
    while start < len(text):
        end = start + size
        chunks.append(text[start:end])
        start = end - overlap
    return [c for c in chunks if c.strip()]


class RetrievalService:
    def __init__(self):
        self._managers: dict[str, FaissManager] = {}

    def _get_manager(self, language: str) -> FaissManager:
        if language not in self._managers:
            self._managers[language] = FaissManager(language)
        return self._managers[language]

    def retrieve(self, query: str, language: str, top_k: int = TOP_K) -> list[tuple[str, float]]:
        manager = self._get_manager(language)
        query_vector = embedding_service.encode_one(query)
        return manager.search(query_vector, top_k)


retrieval_service = RetrievalService()
