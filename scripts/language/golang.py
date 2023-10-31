from typing import List, override

from language.language import Language
from pojo.day import Day


class Go(Language):
    @property
    @override
    def name(self) -> str:
        return "golang"

    @property
    @override
    def solution_file(self) -> str:
        return "solver.go"

    @override
    def _run_setup(self) -> None:
        pass

    @override
    def compile(self) -> None:
        # For now we use go run, which both compiles and runs our code
        pass

    @override
    def _get_run_command(self, day: Day, run_args: List[str]) -> List[str]:
        return ["go", "run", self.solution_file]

    @override
    def template_processing(self, day: Day) -> None:
        # No additional template processing needed
        pass
