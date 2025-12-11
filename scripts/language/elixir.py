import os
from dataclasses import dataclass

from pojo.day import Day


@dataclass(frozen=True)
class Elixir:
    name: str = "elixir"
    file: str = "solver.ex"
    cmd: str = "mix"

    def build(self) -> list[list[str]]:
        return []

    def test(self) -> list[str]:
        # no unit tests
        return []

    def run(self, day: Day, args: list[str]) -> list[str]:
        return ["mix", "solve", day.year, day.day] + args

    def setup(self, day: Day) -> None:
        module = f"Y{day.year}.D{day.day}"
        solution = day.file(self.file)
        os.system(f"sed -i '' -e 's/MODULE/{module}/g' {solution}")
