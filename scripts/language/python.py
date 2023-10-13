import os
from typing import List

from language.language import Language
from pojo.day import Day


class Python(Language):
    @property
    def name(self) -> str:
        return "python"

    @property
    def solution_file(self) -> str:
        return "solver.py"

    def _run_setup(self) -> None:
        os.system("pip install -e ../../commons/python")

    def compile(self) -> None:
        # Interpreted languages do not need to be compiled
        pass

    def _get_run_command(self, day: Day, run_args: List[str]) -> str:
        return f"python {self.solution_file}"

    def template_processing(self, day: Day) -> None:
        # No additional template processing needed
        pass
