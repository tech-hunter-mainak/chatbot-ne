from pathlib import Path
from typing import List

import yaml

from app.models.okf import OKFDocument


class OKFLoader:

    def __init__(self, knowledgeDir: Path):
        self.knowledgeDir = knowledgeDir

    def loadDocuments(self) -> List[OKFDocument]:
        documents = []

        yamlFiles = list(self.knowledgeDir.rglob("*.yaml"))
        yamlFiles.extend(self.knowledgeDir.rglob("*.yml"))

        for filePath in yamlFiles:

            with open(filePath, "r", encoding="utf-8") as file:
                data = yaml.safe_load(file)

            document = OKFDocument.model_validate(data)

            documents.append(document)

        return documents