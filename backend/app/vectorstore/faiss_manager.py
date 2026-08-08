import json
import faiss
import numpy as np

from app.config import VECTOR_DB_DIR


class FaissManager:
    """One FAISS index + metadata file per language. Cosine similarity via normalized vectors + inner product."""

    def __init__(self, language: str):
        self.language = language
        self.index_path = VECTOR_DB_DIR / f"{language}.index"
        self.meta_path = VECTOR_DB_DIR / f"{language}_meta.json"
        self.index = None
        self.chunks: list[str] = []

    def build(self, vectors: np.ndarray, chunks: list[str]):
        dim = vectors.shape[1]
        self.index = faiss.IndexFlatIP(dim)
        self.index.add(vectors)
        self.chunks = chunks
        self._save()

    def load(self) -> bool:
        if not self.index_path.exists() or not self.meta_path.exists():
            return False
        self.index = faiss.read_index(str(self.index_path))
        self.chunks = json.loads(self.meta_path.read_text(encoding="utf-8"))
        return True

    def search(self, query_vector: np.ndarray, top_k: int) -> list[tuple[str, float]]:
        if self.index is None and not self.load():
            return []
        query_vector = query_vector.reshape(1, -1)
        scores, indices = self.index.search(query_vector, top_k)
        results = []
        for score, idx in zip(scores[0], indices[0]):
            if idx == -1:
                continue
            results.append((self.chunks[idx], float(score)))
        return results

    def _save(self):
        faiss.write_index(self.index, str(self.index_path))
        self.meta_path.write_text(json.dumps(self.chunks, ensure_ascii=False), encoding="utf-8")
