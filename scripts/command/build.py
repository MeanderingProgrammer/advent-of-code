from dataclasses import dataclass
from typing import override

from command.command import Command
from component.command import Executor
from language.language import Language


@dataclass(frozen=True)
class LanguageBuild:
    name: str
    build: list[list[str]]
    test: list[str]
    executor: Executor

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
        [self.executor.run(command) for command in self.build]
        print("Testing")
        self.executor.run(self.test)


@dataclass(frozen=True)
class Build(Command):
    languages: list[Language]

    @override
    def info(self) -> dict:
        return {build.key(): build.value() for build in self.builds()}

    @override
    def run(self) -> None:
        [build.execute() for build in self.builds()]

    def builds(self) -> list[LanguageBuild]:
        executor = Executor()
        return [
            LanguageBuild(
                name=language.name,
                build=language.build_commands(),
                test=language.test_command(),
                executor=executor,
            )
            for language in self.languages
        ]
