from enum import Enum


class AvailableLanguages(Enum):
    ENGLISH = 'en'
    FRENCH = 'fr'
    SPANISH = 'es'
    GERMAN = 'de'

    @classmethod
    def list_available_languages(cls) -> list[str]:
        return list(map(lambda c: c.value, cls))
