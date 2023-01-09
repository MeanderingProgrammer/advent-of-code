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

    def get_all(self) -> List[Language]:
        return self.__languages

    def get_by_name(self, name) -> Language:
        mapping = { language.name: language for language in self.__languages }
        if name not in mapping:
            raise Exception(f'{name} is not one of {list(mapping.keys())}')
        return mapping[name]
