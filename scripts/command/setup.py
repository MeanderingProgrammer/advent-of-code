from dataclasses import dataclass
from typing import override

from command.command import Command
from component.command import execute
from language.language import Language


@dataclass(frozen=True)
class LanguageSetup:
    name: str
    commands: list[list[str]]

    def key(self) -> str:
        return self.name

    def value(self) -> list[str]:
        return [" ".join(command) for command in self.commands]

    def execute(self) -> None:
        print(f"Setting up: {self.name}")
        [execute(command) for command in self.commands]


@dataclass(frozen=True)
class Setup(Command):
    languages: list[Language]

    @override
    def info(self) -> dict:
        return {setup.key(): setup.value() for setup in self.__language_setups()}

    @override
    def run(self) -> None:
        [setup.execute() for setup in self.__language_setups()]

    def __language_setups(self) -> list[LanguageSetup]:
        return [
            LanguageSetup(name=language.name, commands=language.setup_commands())
            for language in self.languages
        ]
