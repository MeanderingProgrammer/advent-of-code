from typing import List

from language.language import Language
from pojo.day import Day


class Go(Language):
    @property
    def name(self) -> str:
        return "golang"

    @property
    def solution_file(self) -> str:
        return "solver.go"

    def _run_setup(self) -> None:
        pass

    def compile(self) -> None:
        # For now we use go run, which both compiles and runs our code
        pass

    def _get_run_command(self, day: Day, run_args: List[str]) -> List[str]:
        return ["go", "run", self.solution_file]

    def template_processing(self, day: Day) -> None:
        # No additional template processing needed
        pass
