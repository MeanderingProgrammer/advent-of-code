from dataclasses import dataclass, field
from typing import override

from language.language import Language
from pojo.day import Day


@dataclass(kw_only=True, init=False)
class Python(Language):
    name: str = field(default="python", repr=False)
    solution_file: str = field(default="solver.py", repr=False)
    commons_path: str = field(default="commons/python", repr=False)

    @override
    def cmd(self) -> str:
        return "python"

    @override
    def test_command(self) -> list[str]:
        return ["pytest", "-s", self.commons_path]

    @override
    def build_commands(self) -> list[list[str]]:
        return [["pip", "install", "-q", "-e", self.commons_path]]

    @override
    def run_command(self, day: Day, run_args: list[str]) -> list[str]:
        return ["python", str(self.solution_path(day))] + run_args

    @override
    def add_build(self, day: Day) -> None:
        # No additional build work needed
        pass
