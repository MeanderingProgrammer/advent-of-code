from dataclasses import dataclass
from typing import override

from language.language import Language
from pojo.day import Day


@dataclass
class Java(Language):
    @property
    @override
    def name(self) -> str:
        return "java"

    @property
    @override
    def file(self) -> str:
        return "src/Solver.java"

    @property
    @override
    def cmd(self) -> str:
        # Supports color with --console=rich
        # However it destroys the output
        return "gradle"

    @override
    def test_command(self) -> list[str]:
        return ["./gradlew", "test"]

    @override
    def build_commands(self) -> list[list[str]]:
        return [["./gradlew", "build", "-q"]]

    @override
    def run_command(self, day: Day, args: list[str]) -> list[str]:
        arg = " ".join(args)
        args = [] if len(args) == 0 else [f'--args="{arg}"']
        return ["./gradlew", f":{Java.task(day)}:run", "-q"] + args

    @override
    def add_build(self, day: Day) -> None:
        f = open("settings.gradle.kts", "a")
        f.write("\n")
        f.write(f'include("{Java.task(day)}")\n')
        f.write(f'project(":{Java.task(day)}").projectDir = file("{day.dir()}")\n')
        f.close()

    @staticmethod
    def task(day: Day) -> str:
        return f"{day.year}-{day.day}"
