import os
from typing import List

from language.language import Language
from pojo.day import Day


class Ocaml(Language):
    @property
    def name(self) -> str:
        return "ocaml"

    @property
    def solution_file(self) -> str:
        return "solver.ml"

    def _run_setup(self) -> None:
        os.system("dune build")

    def compile(self) -> None:
        # Since our setup command builds all executable, each day does not
        # need to be individually compiled
        pass

    def _get_run_command(self, day: Day, run_args: List[str]) -> List[str]:
        return ["dune", "exec", f"{day.year}_{day.day}"]

    def template_processing(self, day: Day) -> None:
        # No additional template processing needed
        pass
