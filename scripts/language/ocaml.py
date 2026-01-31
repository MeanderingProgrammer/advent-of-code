from dataclasses import dataclass

from component.command import Executor
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
        binary = Ocaml.binary(day)
        dune = day.dir() / "dune"
        Executor().call(["sed", "-i", "", "-e", f"s/EXEC/{binary}/g", str(dune)])

    @staticmethod
    def binary(day: Day) -> str:
        return f"{day.year}_{day.day}"
