from dataclasses import dataclass
from typing import override

from language.language import Language
from pojo.day import Day


@dataclass
class Go(Language):

    @property
    @override
    def name(self) -> str:
        return "go"

    @property
    @override
    def file(self) -> str:
        return "solver.go"

    @property
    @override
    def cmd(self) -> str:
        # Does not support color output
        return "go"

    @override
    def test_command(self) -> list[str]:
        return ["go", "test", "-v", "./..."]

    @override
    def build_commands(self) -> list[list[str]]:
        # For now we use go run, which both compiles and runs our code
        return []

    @override
    def run_command(self, day: Day, args: list[str]) -> list[str]:
        return ["go", "run", str(self.solution(day))] + args

    @override
    def add_build(self, day: Day) -> None:
        # No additional build work needed
        pass
