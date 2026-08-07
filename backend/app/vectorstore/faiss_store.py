import os
import pickle
from pathlib import Path
from typing import List, Dict, Any, Tuple

import numpy as np

try:
    import faiss
    _HAS_FAISS = True
except Exception:
    _HAS_FAISS = False


class FaissStore:
    def __init__(self, dim: int, persist_dir: Path):
        self.dim = dim
        self.persist_dir = Path(persist_dir)
        self.persist_dir.mkdir(parents=True, exist_ok=True)

        self.index_path = self.persist_dir / "index.faiss"
        self.meta_path = self.persist_dir / "metadata.pkl"

        self.id_mapping: Dict[int, str] = {}
        self.metadata: Dict[str, Dict[str, Any]] = {}

        if _HAS_FAISS:
            if self.index_path.exists():
                self.index = faiss.read_index(str(self.index_path))
                with open(self.meta_path, "rb") as fh:
                    data = pickle.load(fh)
                    self.id_mapping = data.get("id_mapping", {})
                    self.metadata = data.get("metadata", {})
            else:
                self.index = faiss.IndexFlatIP(dim)
        else:
            # fallback: simple numpy store
            self.index = None
            self._embeddings = None

    def add_documents(self, docs: List[Dict[str, Any]]):
        # docs: list of {id, embedding (np.ndarray), metadata}
        if _HAS_FAISS:
            start_idx = len(self.id_mapping)
            vectors = []
            for i, doc in enumerate(docs):
                vectors.append(doc["embedding"].astype("float32"))
                self.id_mapping[start_idx + i] = doc["id"]
                self.metadata[doc["id"]] = doc.get("metadata", {})

            vecs = np.vstack(vectors)
            faiss.normalize_L2(vecs)
            self.index.add(vecs)

            faiss.write_index(self.index, str(self.index_path))
            with open(self.meta_path, "wb") as fh:
                pickle.dump({"id_mapping": self.id_mapping, "metadata": self.metadata}, fh)
        else:
            new_vecs = np.vstack([d["embedding"] for d in docs]).astype("float32")
            if getattr(self, "_embeddings", None) is None:
                self._embeddings = new_vecs
            else:
                self._embeddings = np.vstack([self._embeddings, new_vecs])

            for d in docs:
                self.metadata[d["id"]] = d.get("metadata", {})

    def search(self, query_embedding: np.ndarray, top_k: int = 5) -> List[Tuple[str, float, Dict[str, Any]]]:
        q = query_embedding.astype("float32")
        if _HAS_FAISS:
            faiss.normalize_L2(q.reshape(1, -1))
            distances, indices = self.index.search(q.reshape(1, -1), top_k)
            results = []
            for score, idx in zip(distances[0], indices[0]):
                if idx < 0:
                    continue
                doc_id = self.id_mapping.get(int(idx))
                meta = self.metadata.get(doc_id, {})
                results.append((doc_id, float(score), meta))
            return results
        else:
            # brute force cosine similarity
            from numpy.linalg import norm

            emb = self._embeddings
            q_norm = q / (norm(q) + 1e-12)
            emb_norm = emb / (np.linalg.norm(emb, axis=1, keepdims=True) + 1e-12)
            sims = (emb_norm @ q_norm).reshape(-1)
            idxs = np.argsort(-sims)[:top_k]
            results = []
            for idx in idxs:
                # need mapping from row idx -> id; assume insertion order
                # metadata keys insertion order preserved
                ids = list(self.metadata.keys())
                doc_id = ids[idx]
                results.append((doc_id, float(sims[idx]), self.metadata.get(doc_id, {})))
            return results
