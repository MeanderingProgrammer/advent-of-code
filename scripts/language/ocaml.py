import os
from dataclasses import dataclass, field
from typing import override

from language.language import Language
from pojo.day import Day


@dataclass(kw_only=True, init=False)
class Ocaml(Language):
    name: str = field(default="ocaml", repr=False)
    solution_file: str = field(default="solver.ml", repr=False)

    @override
    def cmd(self) -> str:
        return "dune"

    @override
    def test_command(self) -> list[str]:
        return Ocaml.dune("test")

    @override
    def build_commands(self) -> list[list[str]]:
        return [
            ["opam", "install", "--yes", "--deps-only", "."],
            Ocaml.dune("build"),
        ]

    @override
    def run_command(self, day: Day, run_args: list[str]) -> list[str]:
        return Ocaml.dune("exec") + ["--", Ocaml.binary(day)] + run_args

    @override
    def add_build(self, day: Day) -> None:
        dune_path = day.dir().joinpath("dune")
        os.system(f"sed -i '' -e 's/EXEC/{Ocaml.binary(day)}/g' {dune_path}")

    @staticmethod
    def dune(command: str) -> list[str]:
        return ["dune", command, "--profile", "release"]

    @staticmethod
    def binary(day: Day) -> str:
        return f"{day.year}_{day.day}"
