import hashlib
from typing import Dict


def generateKnowledgeUnitId(
    language: str,
    category: str,
    title: str,
    content: str
) -> str:

    digest = hashlib.sha256(
        content.encode("utf-8")
    ).hexdigest()[:12]

    return f"{category}-{language}-{digest}"


def generateOkf(
    section: Dict,
    metadata: Dict
) -> Dict:

    title = section["title"].strip()

    content = section["content"].strip()

    language = metadata["language"]

    category = metadata["category"]

    knowledgeUnitId = generateKnowledgeUnitId(
        language=language,
        category=category,
        title=title,
        content=content
    )

    okf = {

        "id": knowledgeUnitId,

        "title": title,

        "language": language,

        "category": category,

        "version": metadata.get("version", 1),

        "source": {

            "document": metadata["document_name"],

            "file": metadata["source_file"],

            "author": metadata.get("author", "")
        },

        "metadata": {

            "created": metadata.get("created", ""),

            "modified": metadata.get("modified", ""),

            "tags": metadata.get("tags", [])
        },

        "content": content

    }

    return okf