from pathlib import Path
import argparse

from app.ingestion.detector import LanguageDetector
from app.ingestion.parserFactory import getParser

from app.ingestion.cleaner import cleanText
from app.ingestion.metadata import extractMetadata
from app.ingestion.knowledgeUnitBuilder import buildKnowledgeUnits
from app.ingestion.okfGenerator import generateOkf
from app.ingestion.validator import validateOkf
from app.ingestion.writer import saveKnowledgeUnits


def processFile(
    filePath: Path,
    language: str,
    outputDirectory: Path
):

    print(f"Processing {filePath.name}")

    parser = getParser(filePath)

    document = parser.parse(filePath)

    document["text"] = cleanText(
        document["text"]
    )

    metadata = extractMetadata(
        document,
        language,
        filePath
    )

    knowledgeUnits = buildKnowledgeUnits(
        document,
        metadata
    )

    saved = 0

    for section in knowledgeUnits:

        okf = generateOkf(
            section,
            metadata
        )

        valid, errors = validateOkf(okf)

        if not valid:

            print(errors)

            continue

        saveKnowledgeUnits(
            okf,
            outputDirectory
        )

        saved += 1

    print(f"Saved {saved} KUs")


def main():

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--input",
        required=True
    )

    parser.add_argument(
        "--language",
        required=True
    )

    parser.add_argument(
        "--output",
        required=True
    )

    args = parser.parse_args()

    files = LanguageDetector().detectFiles(
        Path(args.input)
    )

    print(f"Found {len(files)} files")

    for filePath in files:

        processFile(
            filePath,
            args.language,
            Path(args.output)
        )

    print("Completed")


if __name__ == "__main__":

    main()