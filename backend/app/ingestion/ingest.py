from pathlib import Path
import argparse

from backend.app.models import okf
from detector import detectFiles
from parserFactory import getParser
from cleaner import cleanText
from metadata import extractMetadata
from sectionSplitter import splitDocument
from okfGenerator import generateOkf
from validator import validateOkf
from writer import saveKnowledgeUnits


SUPPORTED_EXTENSIONS = {
    ".pdf",
    ".doc",
    ".docx",
    ".txt",
    ".md",
    ".yaml",
    ".yml",
    ".html",
    ".htm"
}


def processFile(filePath: Path, language: str, outputDirectory: Path):

    print(f"Processing: {filePath}")

    parser = getParser(filePath)

    if parser is None:
        print(f"Unsupported file: {filePath}")
        return

    document = parser.parse(filePath)

    if not document:
        print(f"Unable to parse: {filePath}")
        return

    document["text"] = cleanText(document["text"])

    metadata = extractMetadata(
        document=document,
        language=language,
        filePath=filePath
    )

    sections = splitDocument(
        document=document,
        metadata=metadata
    )

    for section in sections:

        okf = generateOkf(
            section=section,
            metadata=metadata
        )

        valid, errors = validateOkf(okf)

        if valid:
            saveKnowledgeUnits(
                okf,
                outputDirectory
            )
        else:
            print("\nValidation Failed")

            for error in errors:
                print(error)


def processDirectory(
    inputDirectory: Path,
    language: str,
    outputDirectory: Path
):

    files = detectFiles(
        directory=inputDirectory,
        supportedExtensions=SUPPORTED_EXTENSIONS
    )

    print(f"Found {len(files)} files.")

    for filePath in files:
        processFile(
            filePath=filePath,
            language=language,
            outputDirectory=outputDirectory
        )

    print("Knowledge generation completed.")


def main():

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--input",
        required=True,
        help="Input directory"
    )

    parser.add_argument(
        "--language",
        required=True,
        help="Language code (asm, kha, lus...)"
    )

    parser.add_argument(
        "--output",
        required=True,
        help="Knowledge directory"
    )

    args = parser.parse_args()

    processDirectory(
        inputDirectory=Path(args.input),
        language=args.language,
        outputDirectory=Path(args.output)
    )


if __name__ == "__main__":
    main()