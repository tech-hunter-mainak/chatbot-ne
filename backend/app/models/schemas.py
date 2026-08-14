from pydantic import BaseModel, Field
from typing import Optional


class ChatRequest(BaseModel):
    query: str = Field(..., description="User question")
    language: str = Field(..., description="Language code, e.g. 'asm', 'kha', 'grt', 'lus'")
    session_id: Optional[str] = Field(None, description="Optional client session id for memory/history")


class SourceChunk(BaseModel):
    text: str
    score: float


class ChatResponse(BaseModel):
    answer: str
    language: str
    sources: list[SourceChunk] = []
