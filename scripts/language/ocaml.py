import os
from dataclasses import dataclass, field
from typing import List, override

from language.language import Language
from pojo.day import Day


@dataclass(kw_only=True, init=False)
class Ocaml(Language):
    name: str = field(default="ocaml", repr=False)
    solution_file: str = field(default="solver.ml", repr=False)

    @override
    def _setup_command(self) -> List[str]:
        return ["dune", "build"]

    @override
    def _run_command(self, day: Day, _: List[str]) -> List[str]:
        return ["dune", "exec", Ocaml.binary(day)]

    @override
    def template_processing(self, day: Day) -> None:
        dune_path = day.dir().joinpath("dune")
        os.system(f"sed -i '' -e 's/EXEC/{Ocaml.binary(day)}/g' {dune_path}")

    @staticmethod
    def binary(day: Day) -> str:
        return f"{day.year}_{day.day}"
