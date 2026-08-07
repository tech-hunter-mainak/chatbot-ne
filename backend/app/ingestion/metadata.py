from pathlib import Path
from typing import Dict
import re


CATEGORY_KEYWORDS = {
    "government": [
        "scheme",
        "government",
        "ministry",
        "department",
        "certificate",
        "application",
        "notification",
        "act",
        "policy"
    ],

    "education": [
        "chapter",
        "lesson",
        "exercise",
        "class",
        "student",
        "teacher",
        "curriculum"
    ],

    "health": [
        "hospital",
        "health",
        "medicine",
        "doctor",
        "disease",
        "vaccination"
    ],

    "tourism": [
        "tourism",
        "park",
        "museum",
        "festival",
        "heritage",
        "temple",
        "wildlife"
    ],

    "agriculture": [
        "farmer",
        "crop",
        "soil",
        "fertilizer",
        "agriculture"
    ]
}


def detectCategory(text: str) -> str:

    text = text.lower()

    scores = {}

    for category, words in CATEGORY_KEYWORDS.items():

        score = 0

        for word in words:

            score += len(re.findall(rf"\b{re.escape(word)}\b", text))

        scores[category] = score

    if max(scores.values()) == 0:
        return "general"

    return max(scores, key=scores.get)


def extractMetadata(
    document: Dict,
    language: str,
    filePath: Path
) -> Dict:

    title = document["title"].strip()

    text = document["text"][:5000]

    category = detectCategory(
        title + "\n" + text
    )

    metadata = {

        "language": language,

        "title": title,

        "category": category,

        "source_file": str(filePath),

        "file_type": document["file_type"],

        "document_name": document["file_name"],

        "author": document.get("author", ""),

        "created": document.get("created", ""),

        "modified": document.get("modified", ""),

        "tags": [],

        "version": 1
    }

    return metadata