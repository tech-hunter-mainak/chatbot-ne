from pathlib import Path
import re

import yaml


def sanitizeName(name: str) -> str:

    name = name.lower()

    name = re.sub(r"[^\w\s-]", "", name)

    name = name.replace(" ", "_")

    name = re.sub(r"_+", "_", name)

    return name.strip("_")


def saveKnowledgeUnits(
    okf: dict,
    outputDirectory: Path
):

    language = okf["language"]

    category = okf["category"]

    documentName = sanitizeName(
        Path(
            okf["source"]["document"]
        ).stem
    )

    sectionName = sanitizeName(
        okf["title"]
    )

    targetDirectory = (
        outputDirectory /
        language /
        category /
        documentName
    )

    targetDirectory.mkdir(
        parents=True,
        exist_ok=True
    )

    filePath = targetDirectory / f"{sectionName}.yaml"

    counter = 1

    while filePath.exists():

        filePath = targetDirectory / f"{sectionName}_{counter}.yaml"

        counter += 1

    with open(
        filePath,
        "w",
        encoding="utf-8"
    ) as file:

        yaml.safe_dump(
            okf,
            file,
            allow_unicode=True,
            sort_keys=False
        )