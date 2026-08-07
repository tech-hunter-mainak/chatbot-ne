from dataclasses import dataclass, field
from typing import Any, Dict, List


@dataclass
class DocumentBlock:

    type: str

    text: str

    level: int = 0

    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Document:

    title: str

    source: str

    fileType: str

    language: str

    author: str = ""

    created: str = ""

    modified: str = ""

    blocks: List[DocumentBlock] = field(default_factory=list)

    metadata: Dict[str, Any] = field(default_factory=dict)