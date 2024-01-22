from language.go import Go
from language.java import Java
from language.language import Language
from language.ocaml import Ocaml
from language.python import Python
from language.rust import Rust


class LanguageFactory:
    def __init__(self):
        self.languages: list[Language] = [
            Go(),
            Java(),
            Ocaml(),
            Python(),
            Rust(),
        ]

    def get_names(self) -> list[str]:
        return [language.name for language in self.languages]

    def get_all(self) -> list[Language]:
        return self.languages

    def get_by_name(self, name: str) -> Language:
        for language in self.languages:
            if language.name == name:
                return language
        raise Exception(f"Could not find language with name: {name}")
