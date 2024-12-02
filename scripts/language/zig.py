from dataclasses import dataclass, field
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
        # TODO - add tests
        return []

    @override
    def build_commands(self) -> list[list[str]]:
        # TODO - separate build command?
        return []

    @override
    def run_command(self, day: Day, run_args: list[str]) -> list[str]:
        # TODO - use run args
        return ["zig", "build", "-Doptimize=ReleaseSafe", f"{day.year}_{day.day}"]

    @override
    def template_processing(self, day: Day) -> None:
        # TODO - update build.zig
        pass
