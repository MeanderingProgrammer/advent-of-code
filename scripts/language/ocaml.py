import os
from typing import List, override

from language.language import Language
from pojo.day import Day


class Ocaml(Language):
    @property
    @override
    def name(self) -> str:
        return "ocaml"

    @property
    @override
    def solution_file(self) -> str:
        return "solver.ml"

    @override
    def _run_setup(self) -> None:
        os.system("dune build")

    @override
    def compile(self) -> None:
        # Since our setup command builds all executable, each day does not
        # need to be individually compiled
        pass

    @override
    def _get_run_command(self, day: Day, _: List[str]) -> List[str]:
        return ["dune", "exec", Ocaml.binary(day)]

    @override
    def template_processing(self, day: Day) -> None:
        dune_path = day.dir().joinpath("dune")
        os.system(f"sed -i '' -e 's/EXEC/{Ocaml.binary(day)}/g' {dune_path}")

    @staticmethod
    def binary(day: Day) -> str:
        return f"{day.year}_{day.day}"
