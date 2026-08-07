from pathlib import Path
from datetime import datetime

from bs4 import BeautifulSoup

from .baseParser import BaseParser


class HtmlParser(BaseParser):

    def parse(self, filePath: Path) -> dict:

        with open(
            filePath,
            "r",
            encoding="utf-8",
            errors="ignore"
        ) as file:

            html = file.read()

        soup = BeautifulSoup(
            html,
            "lxml"
        )

        # Remove unwanted tags
        for tag in soup([
            "script",
            "style",
            "noscript",
            "iframe"
        ]):
            tag.decompose()

        title = ""

        if soup.title:
            title = soup.title.get_text(strip=True)

        if not title:

            heading = soup.find(
                ["h1", "h2", "h3"]
            )

            if heading:
                title = heading.get_text(
                    " ",
                    strip=True
                )

        if not title:
            title = filePath.stem.replace(
                "_",
                " "
            ).replace(
                "-",
                " "
            )

        textParts = []

        for element in soup.find_all([
            "h1",
            "h2",
            "h3",
            "h4",
            "h5",
            "h6",
            "p",
            "li"
        ]):

            text = element.get_text(
                " ",
                strip=True
            )

            if text:
                textParts.append(text)

        # Extract tables
        for table in soup.find_all("table"):

            rows = []

            for row in table.find_all("tr"):

                cells = []

                for cell in row.find_all([
                    "th",
                    "td"
                ]):

                    cells.append(
                        cell.get_text(
                            " ",
                            strip=True
                        )
                    )

                if cells:
                    rows.append(
                        " | ".join(cells)
                    )

            if rows:
                textParts.append(
                    "\n".join(rows)
                )

        stat = filePath.stat()

        return {

            "title": title,

            "text": "\n\n".join(textParts),

            "source": str(filePath),

            "file_name": filePath.name,

            "file_type": "html",

            "extension": filePath.suffix.lower(),

            "author": "",

            "created": datetime.fromtimestamp(
                stat.st_ctime
            ).isoformat(),

            "modified": datetime.fromtimestamp(
                stat.st_mtime
            ).isoformat(),

            "size": stat.st_size
        }