from fastapi import FastAPI, BackgroundTasks
from pydantic import BaseModel
from pathlib import Path

from app.config import SUPPORTED_LANGUAGES, VECTOR_DB_DIR, KNOWLEDGE_DIR
from app.services.okf_indexer import OKFIndexer
from app.services.llm_service import LLMService


app = FastAPI(
    title="NE RAG Chatbot API",
    version="1.0.0",
    description="RAG + OKF based multilingual chatbot for Northeast Indian languages."
)


@app.get("/")
async def root():
    return {"message": "NE RAG Chatbot API is running."}


@app.get("/health")
async def health():
    return {"status": "healthy"}


@app.get("/languages")
async def languages():
    return SUPPORTED_LANGUAGES


class IndexRequest(BaseModel):
    knowledge_path: str = str(KNOWLEDGE_DIR)


@app.post("/index-okf")
async def index_okf(req: IndexRequest, background: BackgroundTasks):
    path = Path(req.knowledge_path)
    indexer = OKFIndexer(persist_dir=VECTOR_DB_DIR)

    def run_index():
        count = indexer.index_directory(path)
        return count

    # run in background for now
    background.add_task(run_index)
    return {"status": "indexing_started", "path": str(path)}


class QueryRequest(BaseModel):
    query: str
    top_k: int = 5
    language: str | None = None


@app.post("/query")
async def query(req: QueryRequest):
    indexer = OKFIndexer(persist_dir=VECTOR_DB_DIR)
    hits = indexer.search(req.query, top_k=req.top_k)

    # If a language is requested, prefer hits in that language
    filtered_hits = hits
    if req.language:
        filtered = [h for h in hits if h[2].get("language") == req.language]
        if filtered:
            filtered_hits = filtered

    # build context from retrieved hits
    context_texts = []
    for doc_id, score, meta in filtered_hits:
        title = meta.get("title", "")
        summary = meta.get("summary", "")
        context_texts.append(f"Title: {title}\nSummary: {summary}")

    # language instruction for the LLM
    lang_instr = ""
    if req.language:
        lang_name = SUPPORTED_LANGUAGES.get(req.language, req.language)
        lang_instr = f"Respond in {lang_name}."

    prompt = (
        f"Use the following context to answer the question. {lang_instr}\n\n"
        f"{chr(10).join(context_texts)}\n\nQuestion: {req.query}\nAnswer:"
    )

    llm = LLMService()
    answer = await llm.generate(prompt)

    return {"answer": answer, "hits": filtered_hits}