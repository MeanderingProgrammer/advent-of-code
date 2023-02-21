from typing import List

from language.golang import Go
from language.java import Java
from language.language import Language
from language.python import Python
from language.rust import Rust


class LanguageFactory:

    def __init__(self) -> str:
        self.__languages = [
            Go(),
            Java(),
            Python(),
            Rust(),
        ]

    def get_names(self) -> List[str]:
        return [language.name for language in self.__languages]

    def get_all(self) -> List[Language]:
        return self.__languages

    def get_by_name(self, name: str) -> Language:
        for language in self.__languages:
            if language.name == name:
                return language
