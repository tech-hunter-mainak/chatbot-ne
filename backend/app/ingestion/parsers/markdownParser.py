from pathlib import Path
from datetime import datetime

from markdown_it import MarkdownIt

from .baseParser import BaseParser


class MarkdownParser(BaseParser):

    def parse(self, filePath: Path) -> dict:

        with open(
            filePath,
            "r",
            encoding="utf-8",
            errors="ignore"
        ) as file:

            markdownText = file.read()

        md = MarkdownIt()

        tokens = md.parse(markdownText)

        title = ""

        textParts = []

        skipNextInline = False

        for index, token in enumerate(tokens):

            if skipNextInline:
                skipNextInline = False
                continue

            if token.type == "heading_open":

                if index + 1 < len(tokens):

                    inlineToken = tokens[index + 1]

                    if inlineToken.type == "inline":

                        heading = inlineToken.content.strip()

                        if heading:

                            if not title:
                                title = heading

                            textParts.append(heading)

                        skipNextInline = True

            elif token.type == "paragraph_open":

                if index + 1 < len(tokens):

                    inlineToken = tokens[index + 1]

                    if inlineToken.type == "inline":

                        paragraph = inlineToken.content.strip()

                        if paragraph:
                            textParts.append(paragraph)

                        skipNextInline = True

            elif token.type == "fence":

                if token.content.strip():

                    textParts.append(token.content.strip())

            elif token.type == "blockquote_open":

                continue

            elif token.type == "bullet_list_open":

                continue

            elif token.type == "ordered_list_open":

                continue

            elif token.type == "list_item_open":

                continue

            elif token.type == "inline":

                continue

        if not title:

            title = filePath.stem.replace(
                "_",
                " "
            ).replace(
                "-",
                " "
            )

        stat = filePath.stat()

        return {

            "title": title,

            "text": "\n\n".join(textParts),

            "source": str(filePath),

            "file_name": filePath.name,

            "file_type": "markdown",

            "extension": ".md",

            "author": "",

            "created": datetime.fromtimestamp(
                stat.st_ctime
            ).isoformat(),

            "modified": datetime.fromtimestamp(
                stat.st_mtime
            ).isoformat(),

            "size": stat.st_size
        }