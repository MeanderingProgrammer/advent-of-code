from dataclasses import dataclass

from component.command import execute
from language.language import Language


@dataclass(frozen=True)
class Setup:
    languages: list[Language]

    def run(self) -> None:
        for language in self.languages:
            print(f"Setting up: {language.name}")
            [execute(command) for command in language.setup_commands()]
