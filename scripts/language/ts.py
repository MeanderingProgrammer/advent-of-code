from dataclasses import dataclass
from typing import override

from language.language import Language
from pojo.day import Day


@dataclass
class TypeScript(Language):
    @property
    @override
    def name(self) -> str:
        return "ts"

    @property
    @override
    def file(self) -> str:
        return "solver.ts"

    @property
    @override
    def cmd(self) -> str:
        return "bun"

    @override
    def test_command(self) -> list[str]:
        return []

    @override
    def build_commands(self) -> list[list[str]]:
        return [["bun", "install", "--save-text-lockfile"]]

    @override
    def run_command(self, day: Day, args: list[str]) -> list[str]:
        return ["bun", "run", str(self.solution(day))] + args

    @override
    def add_build(self, day: Day) -> None:
        # No additional build work needed
        pass
