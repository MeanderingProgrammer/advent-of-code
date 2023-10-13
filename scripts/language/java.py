import os
from typing import List

from language.language import Language
from pojo.day import Day


class Java(Language):
    @property
    def name(self) -> str:
        return "java"

    @property
    def solution_file(self) -> str:
        return "src/Solver.java"

    def _run_setup(self) -> None:
        pass

    def compile(self) -> None:
        os.system("./../../gradlew build -q")

    def _get_run_command(self, day: Day, run_args: List[str]) -> str:
        return "./../../gradlew run -q"

    def template_processing(self, day: Day) -> None:
        # No additional template processing needed
        pass
