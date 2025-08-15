from dataclasses import dataclass
from pathlib import Path

from pojo.day import Day


@dataclass(frozen=True)
class Zig:
    name: str = "zig"
    file: str = "solver.zig"
    cmd: str = "zig"

    def test(self) -> list[str]:
        # currently no unit tests
        return []

    def build(self) -> list[list[str]]:
        # for now use zig build, which both compiles and runs code
        return []

    def run(self, day: Day, args: list[str]) -> list[str]:
        binary = f"{day.year}_{day.day}"
        args = [] if len(args) == 0 else ["--"] + args
        return ["zig", "build", "-Doptimize=ReleaseSmall", binary] + args

    def setup(self, day: Day) -> None:
        path = Path("build.zig")
        contents = path.read_text()
        solutions = contents.split("\n\n")[2].splitlines()[1:-1]
        old = "\n".join(solutions)
        solutions.append(f'    .{{ .year = "{day.year}", .day = "{day.day}" }},')
        solutions.sort()
        new = "\n".join(solutions)
        path.write_text(contents.replace(old, new))
