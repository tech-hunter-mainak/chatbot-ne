from app.config import SUPPORTED_LANGUAGES


class LanguageDetector:

    def __init__(self):
        self.supportedLanguages = SUPPORTED_LANGUAGES

    def detect(self, language: str) -> str:
        """
        For the MVP, the frontend provides the language code.
        This method validates and returns it.

        Future versions can replace this with automatic
        language detection without changing the rest
        of the backend.
        """

        language = language.strip().lower()

        if language not in self.supportedLanguages:
            raise ValueError(
                f"Unsupported language: {language}"
            )

        return language

    def isSupported(self, language: str) -> bool:
        return language.lower() in self.supportedLanguages

    def getSupportedLanguages(self):
        return self.supportedLanguages