from typing import Dict, List, Tuple


SUPPORTED_LANGUAGES = {
    "asm",
    "kha",
    "grt",
    "lus",
    "nag",
    "trp",
    "ccp",
    "wao"
}


SUPPORTED_CATEGORIES = {
    "government",
    "education",
    "health",
    "tourism",
    "agriculture",
    "history",
    "culture",
    "wildlife",
    "citizen_services",
    "faq",
    "general"
}


def validateOkf(okf: Dict) -> Tuple[bool, List[str]]:

    errors = []

    requiredFields = [
        "id",
        "title",
        "language",
        "category",
        "content",
        "source",
        "metadata"
    ]

    for field in requiredFields:

        if field not in okf:
            errors.append(f"Missing field: {field}")

    if errors:
        return False, errors

    if not okf["id"].strip():
        errors.append("Empty ID")

    if not okf["title"].strip():
        errors.append("Empty title")

    if not okf["content"].strip():
        errors.append("Empty content")

    language = okf["language"].lower()

    if language not in SUPPORTED_LANGUAGES:
        errors.append(
            f"Unsupported language: {language}"
        )

    category = okf["category"].lower()

    if category not in SUPPORTED_CATEGORIES:
        errors.append(
            f"Unsupported category: {category}"
        )

    if "document" not in okf["source"]:
        errors.append("Missing source.document")

    if "file" not in okf["source"]:
        errors.append("Missing source.file")

    return len(errors) == 0, errors