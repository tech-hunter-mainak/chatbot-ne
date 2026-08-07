from pathlib import Path
from datetime import datetime

import fitz

from .baseParser import BaseParser


class PdfParser(BaseParser):

    def parse(self, filePath: Path) -> dict:

        document = fitz.open(filePath)

        pages = []

        metadata = document.metadata

        for pageNumber in range(document.page_count):

            page = document.load_page(pageNumber)

            text = page.get_text("text")

            pages.append(text)

        document.close()

        stat = filePath.stat()

        title = metadata.get("title")

        if not title:
            title = filePath.stem.replace("_", " ").replace("-", " ")

        return {

            "title": title,

            "text": "\n\n".join(pages),

            "source": str(filePath),

            "file_name": filePath.name,

            "file_type": "pdf",

            "extension": ".pdf",

            "author": metadata.get("author", ""),

            "created": datetime.fromtimestamp(
                stat.st_ctime
            ).isoformat(),

            "modified": datetime.fromtimestamp(
                stat.st_mtime
            ).isoformat(),

            "size": stat.st_size,

            "page_count": len(pages)
        }