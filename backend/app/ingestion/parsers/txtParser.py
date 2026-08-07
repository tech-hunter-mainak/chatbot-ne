from pathlib import Path
from datetime import datetime

from .baseParser import BaseParser


class TxtParser(BaseParser):

    def parse(self, filePath: Path) -> dict:

        with open(
            filePath,
            "r",
            encoding="utf-8",
            errors="ignore"
        ) as file:
            text = file.read()

        stat = filePath.stat()

        title = filePath.stem.replace("_", " ").replace("-", " ")

        return {
            "title": title,

            "text": text,

            "source": str(filePath),

            "file_name": filePath.name,

            "file_type": "txt",

            "extension": ".txt",

            "author": "",

            "created": datetime.fromtimestamp(
                stat.st_ctime
            ).isoformat(),

            "modified": datetime.fromtimestamp(
                stat.st_mtime
            ).isoformat(),

            "size": stat.st_size
        }