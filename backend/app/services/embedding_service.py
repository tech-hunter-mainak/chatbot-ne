import numpy as np
from sentence_transformers import SentenceTransformer

from app.config import EMBEDDING_MODEL


class EmbeddingService:
    """Thin wrapper around a sentence-transformers model. Loaded once, reused everywhere."""

    _model = None

    def __init__(self):
        if EmbeddingService._model is None:
            EmbeddingService._model = SentenceTransformer(EMBEDDING_MODEL)
        self.model = EmbeddingService._model

    def encode(self, texts: list[str]) -> np.ndarray:
        vectors = self.model.encode(texts, convert_to_numpy=True, normalize_embeddings=True)
        return vectors.astype("float32")

    def encode_one(self, text: str) -> np.ndarray:
        return self.encode([text])[0]


embedding_service = EmbeddingService()
