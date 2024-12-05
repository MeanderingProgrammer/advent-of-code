from dataclasses import dataclass, field
from pathlib import Path
from typing import override

from language.language import Language
from pojo.day import Day


@dataclass(kw_only=True, init=False)
class Zig(Language):
    name: str = field(default="zig", repr=False)
    solution_file: str = field(default="solver.zig", repr=False)

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
    def run_command(self, day: Day, run_args: list[str]) -> list[str]:
        binary = f"{day.year}_{day.day}"
        args = [] if len(run_args) == 0 else ["--"] + run_args
        return ["zig", "build", "-Doptimize=ReleaseSmall", binary] + args

    @override
    def template_processing(self, day: Day) -> None:
        path = Path("build.zig")
        contents = path.read_text()
        solutions = contents.split("\n\n")[1].splitlines()[1:-1]
        old = "\n".join(solutions)
        solutions.append(f'    .{{ "{day.year}", "{day.day}" }},')
        solutions.sort()
        new = "\n".join(solutions)
        path.write_text(contents.replace(old, new))
