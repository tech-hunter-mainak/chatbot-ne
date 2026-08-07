import numpy as np
from typing import Optional

from app.models.okf import OKFDocument
from app.config import EMBEDDING_MODEL


class EmbeddingService:
    def __init__(self):
        self.model = None
        self._load_model()

    def _load_model(self):
        try:
            from sentence_transformers import SentenceTransformer

            self.model = SentenceTransformer(EMBEDDING_MODEL, trust_remote_code=True)
        except Exception:
            # Do not fail import time; raise when generation is attempted.
            self.model = None

    def _ensure_model(self):
        if self.model is None:
            # Try to load again to give clearer error at runtime
            self._load_model()
            if self.model is None:
                raise RuntimeError(
                    "SentenceTransformers model not available. Install 'sentence-transformers' or configure EMBEDDING_MODEL."
                )

    def buildDocumentText(self, document: OKFDocument) -> str:
        return f"""
Title:
{document.title}

Summary:
{document.summary}

Content:
{document.content}

Keywords:
{", ".join(document.keywords)}

Category:
{document.category}
""".strip()

    def generateEmbedding(self, text: str) -> np.ndarray:
        self._ensure_model()

        embedding = self.model.encode(
            text, normalize_embeddings=True, convert_to_numpy=True
        )
        return embedding.astype("float32")

    def generateDocumentEmbedding(self, document: OKFDocument) -> np.ndarray:
        text = self.buildDocumentText(document)
        return self.generateEmbedding(text)