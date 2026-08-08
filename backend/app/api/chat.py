from fastapi import APIRouter, HTTPException

from app.models.schemas import ChatRequest, ChatResponse
from app.services.rag_service import rag_service

router = APIRouter()


@router.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    try:
        return rag_service.answer(request.query, request.language)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
