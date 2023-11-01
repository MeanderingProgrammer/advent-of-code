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
    def _setup_command(self) -> List[str]:
        # For now we use go run, which both compiles and runs our code
        return []

    @override
    def _run_command(self, day: Day, _: List[str]) -> List[str]:
        return ["go", "run", str(day.dir().joinpath(self.solution_file))]

    @override
    def template_processing(self, _: Day) -> None:
        # No additional template processing needed
        pass
