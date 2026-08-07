from app.config import KNOWLEDGE_DIR
from app.services.okf_loader import OKFLoader

loader = OKFLoader(KNOWLEDGE_DIR)

documents = loader.loadDocuments()

print(f"Loaded {len(documents)} documents.\n")

for document in documents:
    print(document.title)
    print(document.language)
    print(document.category)
    print("-" * 40)