import os
from typing import List

from language.language import InterprettedLanguage
from pojo.day import Day


class Python(InterprettedLanguage):
    @property
    def name(self) -> str:
        return "python"

    @property
    def solution_file(self) -> str:
        return "solver.py"

    def _run_setup(self) -> None:
        pwd = os.environ["PWD"]
        os.environ["PYTHONPATH"] = f"{pwd}/commons/python/"

    def _get_run_command(self, day: Day, run_args: List[str]) -> str:
        return "python3 solver.py"

    def template_processing(self, day: Day) -> None:
        # No additional template processing needed
        pass
