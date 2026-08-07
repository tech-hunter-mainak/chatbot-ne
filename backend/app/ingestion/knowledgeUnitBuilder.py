import re
from typing import Dict, List


HEADING_PATTERNS = [
    r"^#{1,6}\s+.+$",                      # Markdown headings
    r"^\d+(\.\d+)*\s+.+$",                 # 1 Introduction / 2.1 Scope
    r"^[A-Z][A-Z\s]{3,}$",                 # ALL CAPS headings
]


MIN_SECTION_LENGTH = 300


def isHeading(line: str) -> bool:

    line = line.strip()

    if not line:
        return False

    for pattern in HEADING_PATTERNS:
        if re.match(pattern, line):
            return True

    return False


def buildKnowledgeUnits(
    document: Dict,
    metadata: Dict
) -> List[Dict]:

    lines = document["text"].split("\n")

    sections = []

    currentTitle = metadata["title"]

    currentContent = []

    for line in lines:

        if isHeading(line):

            if len("\n".join(currentContent).strip()) > MIN_SECTION_LENGTH:

                sections.append({
                    "title": currentTitle,
                    "content": "\n".join(currentContent).strip()
                })

            currentTitle = line.strip("# ").strip()

            currentContent = []

        else:

            currentContent.append(line)

    if currentContent:

        sections.append({
            "title": currentTitle,
            "content": "\n".join(currentContent).strip()
        })

    return sections
