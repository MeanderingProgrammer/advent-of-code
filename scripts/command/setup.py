from dataclasses import dataclass
from typing import override

from command.command import Command
from component.command import execute
from language.language import Language


@dataclass(frozen=True)
class LanguageSetup:
    name: str
    build: list[list[str]]
    test: list[str]

    def key(self) -> str:
        return self.name

    def value(self) -> dict[str, str]:
        return dict(
            build=" && ".join([" ".join(command) for command in self.build]),
            test=" ".join(self.test),
        )

    def execute(self) -> None:
        print(f"Setting up: {self.name}")
        print("Building")
        [execute(command) for command in self.build]
        print("Testing")
        execute(self.test)


@dataclass(frozen=True)
class Setup(Command):
    languages: list[Language]

    @override
    def info(self) -> dict:
        return {setup.key(): setup.value() for setup in self.__setups()}

    @override
    def run(self) -> None:
        [setup.execute() for setup in self.__setups()]

    def __setups(self) -> list[LanguageSetup]:
        return [
            LanguageSetup(
                name=language.name,
                build=language.build_commands(),
                test=language.test_command(),
            )
            for language in self.languages
        ]
