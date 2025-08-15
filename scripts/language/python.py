from dataclasses import dataclass

from pojo.day import Day


@dataclass(frozen=True)
class Python:
    name: str = "python"
    file: str = "solver.py"
    cmd: str = "python"

    def test(self) -> list[str]:
        return ["pytest", "-s", Python.commons()]

    def build(self) -> list[list[str]]:
        return [["pip", "install", "-q", "-e", Python.commons()]]

    def run(self, day: Day, args: list[str]) -> list[str]:
        solution = day.file(self.file)
        return ["python", str(solution)] + args

    def setup(self, day: Day) -> None:
        # no additional setup needed
        pass

    @staticmethod
    def commons() -> str:
        return "commons/python"
