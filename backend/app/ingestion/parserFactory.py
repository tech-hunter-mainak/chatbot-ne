from pathlib import Path
import importlib
from typing import Optional


def getParser(filePath: Path) -> Optional[object]:
    """Return a parser instance for the given file path.

    Parsers are imported lazily to avoid importing heavy native
    dependencies (e.g. PDF libraries) at module import time.
    """

    extension = filePath.suffix.lower()

    mapping = {
        ".pdf": ("app.ingestion.parsers.pdfParser", "PdfParser"),
        ".doc": ("app.ingestion.parsers.docParser", "DocParser"),
        ".docx": ("app.ingestion.parsers.docxParser", "DocxParser"),
        ".txt": ("app.ingestion.parsers.txtParser", "TxtParser"),
        ".md": ("app.ingestion.parsers.markdownParser", "MarkdownParser"),
        ".yaml": ("app.ingestion.parsers.yamlParser", "YamlParser"),
        ".yml": ("app.ingestion.parsers.yamlParser", "YamlParser"),
        ".html": ("app.ingestion.parsers.htmlParser", "HtmlParser"),
        ".htm": ("app.ingestion.parsers.htmlParser", "HtmlParser"),
    }

    entry = mapping.get(extension)

    if not entry:
        return None

    module_name, class_name = entry

    try:
        module = importlib.import_module(module_name)
        cls = getattr(module, class_name)
        return cls()
    except Exception:
        return None