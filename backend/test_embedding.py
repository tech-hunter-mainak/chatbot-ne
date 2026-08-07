from app.config import KNOWLEDGE_DIR
from app.services.okf_loader import OKFLoader
from app.services.embedding_service import EmbeddingService

loader = OKFLoader(KNOWLEDGE_DIR)

documents = loader.loadDocuments()

embeddingService = EmbeddingService()

embedding = embeddingService.generateDocumentEmbedding(
    documents[0]
)

print(embedding.shape)
print(embedding.dtype)