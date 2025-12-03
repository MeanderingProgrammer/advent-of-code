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
        solution = day.file(self.file)
        return ["mix", "run", str(solution)] + args

    def setup(self, day: Day) -> None:
        # no additional setup
        pass
