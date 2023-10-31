import os
from typing import List, override

from language.language import Language
from pojo.day import Day


class Python(Language):
    @property
    @override
    def name(self) -> str:
        return "python"

    @property
    @override
    def solution_file(self) -> str:
        return "solver.py"

    @override
    def _run_setup(self) -> None:
        os.system("pip install -q -e ../../commons/python")

    @override
    def compile(self) -> None:
        # Interpreted languages do not need to be compiled
        pass

    @override
    def _get_run_command(self, day: Day, run_args: List[str]) -> List[str]:
        return ["python", self.solution_file]

    @override
    def template_processing(self, day: Day) -> None:
        # No additional template processing needed
        pass
