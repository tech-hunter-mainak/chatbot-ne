import re


def cleanText(text: str) -> str:

    if text is None:
        return ""

    text = text.replace("\r\n", "\n")
    text = text.replace("\r", "\n")

    text = text.replace("\t", " ")

    text = re.sub(r"[ ]{2,}", " ", text)

    text = re.sub(r"\n{3,}", "\n\n", text)

    text = re.sub(r"[ ]+\n", "\n", text)

    text = re.sub(r"\n[ ]+", "\n", text)

    text = text.strip()

    return text