from pathlib import Path
from typing import List

import numpy as np

from app.services.embedding_service import EmbeddingService
from app.services.okf_loader import OKFLoader
from app.vectorstore.faiss_store import FaissStore
from app.config import VECTOR_DB_DIR


class OKFIndexer:
    def __init__(self, persist_dir: Path = None):
        self.embedding = EmbeddingService()
        self.persist_dir = persist_dir or VECTOR_DB_DIR

    def index_directory(self, knowledge_dir: Path):
        loader = OKFLoader(knowledge_dir)
        documents = loader.loadDocuments()

        if not documents:
            return 0

        # generate embeddings and prepare docs
        docs_for_index = []
        for doc in documents:
            text = self.embedding.buildDocumentText(doc)
            emb = self.embedding.generateEmbedding(text)
            docs_for_index.append({
                "id": doc.id,
                "embedding": emb,
                "metadata": {
                    "title": doc.title,
                    "summary": doc.summary,
                    "language": doc.language,
                }
            })

        dim = docs_for_index[0]["embedding"].shape[0]
        store = FaissStore(dim=dim, persist_dir=self.persist_dir)
        store.add_documents(docs_for_index)

        return len(docs_for_index)

    def search(self, query: str, top_k: int = 5):
        q_emb = self.embedding.generateEmbedding(query)
        # infer dim and load store
        dim = q_emb.shape[0]
        store = FaissStore(dim=dim, persist_dir=self.persist_dir)
        return store.search(q_emb, top_k=top_k)
