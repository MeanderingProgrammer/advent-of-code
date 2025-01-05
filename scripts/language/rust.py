from dataclasses import dataclass, field
from typing import override

import toml
from language.language import Language
from pojo.day import Day


@dataclass(kw_only=True, init=False)
class Rust(Language):
    name: str = field(default="rust", repr=False)
    solution_file: str = field(default="solver.rs", repr=False)

    @override
    def cmd(self) -> str:
        return "cargo"

    @override
    def test_command(self) -> list[str]:
        return ["cargo", "test", "-rq", "--test", "aoc_lib"]

    @override
    def build_commands(self) -> list[list[str]]:
        return [["cargo", "build", "-rq", "--bins"]]

    @override
    def run_command(self, day: Day, run_args: list[str]) -> list[str]:
        args = [] if len(run_args) == 0 else ["--"] + run_args
        return ["cargo", "run", "-rq", "--bin", Rust.binary(day)] + args

    @override
    def add_build(self, day: Day) -> None:
        cargo_file = "Cargo.toml"
        cargo = toml.load(cargo_file)
        bin_config = dict(
            name=Rust.binary(day),
            path=str(day.dir().joinpath(self.solution_file)),
        )
        if bin_config in cargo["bin"]:
            print("Do not need to update Cargo file")
            return

        cargo["bin"].append(bin_config)
        cargo["bin"].sort(key=lambda bin: bin["name"])

        f = open(cargo_file, "w+")
        f.write(toml.dumps(cargo))
        f.close()

    @staticmethod
    def binary(day: Day) -> str:
        return f"aoc_{day.year}_{day.day}"
