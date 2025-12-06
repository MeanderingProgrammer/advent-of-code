from dataclasses import dataclass
from typing import Final

from pojo.day import Day


@dataclass(frozen=True)
class Python:
    LIB: Final[str] = "lib/python"

    name: str = "python"
    file: str = "solver.py"
    cmd: str = "python"

    def build(self) -> list[list[str]]:
        return [["pip", "install", "-q", "-e", Python.LIB]]

    def test(self) -> list[str]:
        return ["pytest", "-s", Python.LIB]

    def run(self, day: Day, args: list[str]) -> list[str]:
        solution = day.file(self.file)
        return ["python", str(solution)] + args

    def setup(self, day: Day) -> None:
        # no additional setup
        pass
