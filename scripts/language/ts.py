from dataclasses import dataclass, field
from typing import override

from language.language import Language
from pojo.day import Day


@dataclass(kw_only=True, init=False)
class TypeScript(Language):
    name: str = field(default="ts", repr=False)
    solution_file: str = field(default="solver.ts", repr=False)

    @override
    def cmd(self) -> str:
        return "bun"

    @override
    def test_command(self) -> list[str]:
        return []

    @override
    def build_commands(self) -> list[list[str]]:
        return [["bun", "install"]]

    @override
    def run_command(self, day: Day, run_args: list[str]) -> list[str]:
        return ["bun", "run", str(self.solution_path(day))] + run_args

    @override
    def template_processing(self, day: Day) -> None:
        pass
