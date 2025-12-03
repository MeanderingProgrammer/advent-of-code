import shutil

from language.elixir import Elixir
from language.go import Go
from language.java import Java
from language.language import Language
from language.ocaml import Ocaml
from language.python import Python
from language.rust import Rust
from language.ts import TypeScript
from language.zig import Zig


class LanguageFactory:
    def __init__(self):
        languages: list[Language] = [
            Elixir(),
            Go(),
            Java(),
            Ocaml(),
            Python(),
            Rust(),
            TypeScript(),
            Zig(),
        ]
        self.languages: list[Language] = []
        for language in languages:
            if shutil.which(language.cmd) is not None:
                self.languages.append(language)

    def names(self) -> list[str]:
        return [language.name for language in self.languages]

    def resolve(self, languages: tuple[Language, ...]) -> list[Language]:
        return self.languages if len(languages) == 0 else list(languages)

    def get(self, name: str) -> Language | None:
        for language in self.languages:
            if language.name == name:
                return language
        return None
