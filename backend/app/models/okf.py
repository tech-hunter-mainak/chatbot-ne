from typing import List, Optional

from pydantic import BaseModel, Field


class Source(BaseModel):
    name: str
    url: Optional[str] = None
    license: Optional[str] = None


class OKFDocument(BaseModel):
    id: str

    language: str

    category: str

    title: str

    summary: str

    content: str

    keywords: List[str] = Field(default_factory=list)

    tags: List[str] = Field(default_factory=list)

    source: Source

    references: List[str] = Field(default_factory=list)

    last_updated: str