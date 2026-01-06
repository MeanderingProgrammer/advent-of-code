from dataclasses import dataclass

from pojo.day import Day


@dataclass(frozen=True)
class Go:
    name: str = "go"
    file: str = "solver.go"
    cmd: str = "go"

    def build(self) -> list[list[str]]:
        # go run both compiles and executes
        return []

    def test(self) -> list[str]:
        return ["go", "test", "-v", "./..."]

    def run(self, day: Day, args: list[str]) -> list[str]:
        solution = day.dir() / self.file
        return ["go", "run", str(solution)] + args

    def setup(self, day: Day) -> None:
        # no additional setup
        pass
