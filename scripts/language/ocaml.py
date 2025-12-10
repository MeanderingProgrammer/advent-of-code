import os
from dataclasses import dataclass

from pojo.day import Day


@dataclass(frozen=True)
class Ocaml:
    name: str = "ocaml"
    file: str = "solver.ml"
    cmd: str = "opam"

    def build(self) -> list[list[str]]:
        return [
            ["opam", "install", "--yes", "--deps-only", "."],
            ["dune", "build", "--profile", "release"],
        ]

    def test(self) -> list[str]:
        return ["dune", "test", "--profile", "release"]

    def run(self, day: Day, args: list[str]) -> list[str]:
        binary = Ocaml.binary(day)
        return ["dune", "exec", "--profile", "release", "--", binary] + args

    def setup(self, day: Day) -> None:
        dune = day.file("dune")
        os.system(f"sed -i '' -e 's/EXEC/{Ocaml.binary(day)}/g' {dune}")

    @staticmethod
    def binary(day: Day) -> str:
        return f"{day.year}_{day.day}"
