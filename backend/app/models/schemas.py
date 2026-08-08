from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    query: str = Field(..., description="User question")
    language: str = Field(..., description="Language code, e.g. 'asm', 'kha', 'grt', 'lus'")


class SourceChunk(BaseModel):
    text: str
    score: float


class ChatResponse(BaseModel):
    answer: str
    language: str
    sources: list[SourceChunk] = []
