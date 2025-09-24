import os
from dataclasses import dataclass

from pojo.day import Day


@dataclass(frozen=True)
class Ocaml:
    name: str = "ocaml"
    file: str = "solver.ml"
    cmd: str = "opam"

    def test(self) -> list[str]:
        return Ocaml.dune("test")

    def build(self) -> list[list[str]]:
        return [
            ["opam", "install", "--yes", "--deps-only", "."],
            Ocaml.dune("build"),
        ]

    def run(self, day: Day, args: list[str]) -> list[str]:
        return Ocaml.dune("exec") + ["--", Ocaml.binary(day)] + args

    def setup(self, day: Day) -> None:
        dune = day.file("dune")
        os.system(f"sed -i '' -e 's/EXEC/{Ocaml.binary(day)}/g' {dune}")

    @staticmethod
    def dune(command: str) -> list[str]:
        return ["dune", command, "--profile", "release"]

    @staticmethod
    def binary(day: Day) -> str:
        return f"{day.year}_{day.day}"
