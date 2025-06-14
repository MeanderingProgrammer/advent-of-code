from dataclasses import dataclass
from pathlib import Path
from typing import override

from language.language import Language
from pojo.day import Day


@dataclass
class Zig(Language):

    @property
    @override
    def name(self) -> str:
        return "zig"

    @property
    @override
    def file(self) -> str:
        return "solver.zig"

    @property
    @override
    def cmd(self) -> str:
        return "zig"

    @override
    def test_command(self) -> list[str]:
        # Currently no unit tests
        return []

    @override
    def build_commands(self) -> list[list[str]]:
        # For now we use zig build, which both compiles and runs our code
        return []

    @override
    def run_command(self, day: Day, args: list[str]) -> list[str]:
        binary = f"{day.year}_{day.day}"
        args = [] if len(args) == 0 else ["--"] + args
        return ["zig", "build", "-Doptimize=ReleaseSmall", binary] + args

    @override
    def add_build(self, day: Day) -> None:
        path = Path("build.zig")
        contents = path.read_text()
        solutions = contents.split("\n\n")[2].splitlines()[1:-1]
        old = "\n".join(solutions)
        solutions.append(f'    .{{ .year = "{day.year}", .day = "{day.day}" }},')
        solutions.sort()
        new = "\n".join(solutions)
        path.write_text(contents.replace(old, new))
