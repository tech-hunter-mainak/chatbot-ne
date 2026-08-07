import shutil
import subprocess
import tempfile

from pathlib import Path

from .baseParser import BaseParser
from .docxParser import DocxParser


class DocParser(BaseParser):

    def parse(self, filePath: Path) -> dict:

        soffice = shutil.which("soffice")

        if soffice is None:
            raise RuntimeError(
                "LibreOffice (soffice) was not found in PATH."
            )

        with tempfile.TemporaryDirectory() as tempDirectory:

            subprocess.run(
                [
                    soffice,
                    "--headless",
                    "--convert-to",
                    "docx",
                    "--outdir",
                    tempDirectory,
                    str(filePath)
                ],
                check=True
            )

            converted = (
                Path(tempDirectory) /
                (filePath.stem + ".docx")
            )

            if not converted.exists():
                raise RuntimeError(
                    "DOC conversion failed."
                )

            parser = DocxParser()

            return parser.parse(converted)