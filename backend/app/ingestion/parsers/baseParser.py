from abc import ABC, abstractmethod
from pathlib import Path

from app.ingestion.document import Document


class BaseParser(ABC):

    @abstractmethod
    def parse(
        self,
        filePath: Path,
        language: str
    ) -> Document:
        """Parse a document and return a structured Document object."""
        pass