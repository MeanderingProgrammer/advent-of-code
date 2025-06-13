from dataclasses import dataclass
from typing import override

from language.language import Language
from pojo.day import Day


@dataclass
class Python(Language):

    @property
    @override
    def name(self) -> str:
        return "python"

    @property
    @override
    def file(self) -> str:
        return "solver.py"

    @property
    @override
    def cmd(self) -> str:
        return "python"

    @override
    def test_command(self) -> list[str]:
        return ["pytest", "-s", Python.commons()]

    @override
    def build_commands(self) -> list[list[str]]:
        return [["pip", "install", "-q", "-e", Python.commons()]]

    @override
    def run_command(self, day: Day, args: list[str]) -> list[str]:
        return ["python", str(self.solution(day))] + args

    @override
    def add_build(self, day: Day) -> None:
        # No additional build work needed
        pass

    @staticmethod
    def commons() -> str:
        return "commons/python"
