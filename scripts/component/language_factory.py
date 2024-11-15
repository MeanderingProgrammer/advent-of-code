import shutil

from language.go import Go
from language.java import Java
from language.language import Language
from language.ocaml import Ocaml
from language.python import Python
from language.rust import Rust
from language.ts import TypeScript


class LanguageFactory:
    def __init__(self):
        languages: list[Language] = [
            Go(),
            Java(),
            Ocaml(),
            Python(),
            Rust(),
            TypeScript(),
        ]
        self.languages: list[Language] = []
        for language in languages:
            if shutil.which(language.cmd()) is not None:
                self.languages.append(language)

    def get_names(self) -> list[str]:
        return [language.name for language in self.languages]

    def get_all(self) -> list[Language]:
        return self.languages

    def get_by_name(self, name: str) -> Language:
        for language in self.languages:
            if language.name == name:
                return language
        raise Exception(f"Could not find language with name: {name}")
