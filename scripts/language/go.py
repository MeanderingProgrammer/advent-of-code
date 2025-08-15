from dataclasses import dataclass

from pojo.day import Day


@dataclass(frozen=True)
class Go:
    name: str = "go"
    file: str = "solver.go"
    cmd: str = "go"

    def test(self) -> list[str]:
        return ["go", "test", "-v", "./..."]

    def build(self) -> list[list[str]]:
        # for now use go run, which both compiles and runs code
        return []

    def run(self, day: Day, args: list[str]) -> list[str]:
        solution = day.file(self.file)
        return ["go", "run", str(solution)] + args

    def setup(self, day: Day) -> None:
        # no additional setup needed
        pass
