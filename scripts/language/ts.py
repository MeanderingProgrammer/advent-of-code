from dataclasses import dataclass

from pojo.day import Day


@dataclass(frozen=True)
class TypeScript:
    name: str = "ts"
    file: str = "solver.ts"
    cmd: str = "bun"

    def test(self) -> list[str]:
        return []

    def build(self) -> list[list[str]]:
        return [["bun", "install", "--save-text-lockfile"]]

    def run(self, day: Day, args: list[str]) -> list[str]:
        solution = day.file(self.file)
        return ["bun", "run", str(solution)] + args

    def setup(self, day: Day) -> None:
        # no additional setup needed
        pass
