from dataclasses import dataclass, field
from typing import override

from language.language import Language
from pojo.day import Day


@dataclass(kw_only=True, init=False)
class Go(Language):
    name: str = field(default="golang", repr=False)
    solution_file: str = field(default="solver.go", repr=False)

    @override
    def _setup_commands(self) -> list[list[str]]:
        # For now we use go run, which both compiles and runs our code
        return []

    @override
    def run_command(self, day: Day, run_args: list[str]) -> list[str]:
        return ["go", "run", str(self.solution_path(day))] + run_args

    @override
    def template_processing(self, _: Day) -> None:
        # No additional template processing needed
        pass
