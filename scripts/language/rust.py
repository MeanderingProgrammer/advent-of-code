from dataclasses import dataclass, field
from pathlib import Path
from typing import override

import tomlkit
from language.language import Language
from pojo.day import Day
from tomlkit.items import AoT


@dataclass(kw_only=True, init=False)
class Rust(Language):
    name: str = field(default="rust", repr=False)
    solution_file: str = field(default="solver.rs", repr=False)

    @override
    def cmd(self) -> str:
        return "cargo"

    @override
    def test_command(self) -> list[str]:
        return Rust.cargo("test") + ["--test", "aoc"]

    @override
    def build_commands(self) -> list[list[str]]:
        return [Rust.cargo("build") + ["--bins"]]

    @override
    def run_command(self, day: Day, run_args: list[str]) -> list[str]:
        args = [] if len(run_args) == 0 else ["--"] + run_args
        return Rust.cargo("run") + ["--bin", Rust.binary(day)] + args

    @override
    def add_build(self, day: Day) -> None:
        config = tomlkit.table()
        config["name"] = Rust.binary(day)
        config["path"] = str(day.dir().joinpath(self.solution_file))

        path = Path("Cargo.toml")
        cargo = tomlkit.parse(path.read_text())
        bins = cargo["bin"]
        assert isinstance(bins, AoT)
        if config in bins:
            print("Do not need to update Cargo file")
            return

        bins.append(config)
        cargo["bin"] = sorted(bins, key=lambda bin: bin["name"])
        path.write_text(cargo.as_string())

    @staticmethod
    def cargo(command: str) -> list[str]:
        return ["cargo", command, "-rq"]

    @staticmethod
    def binary(day: Day) -> str:
        return f"aoc_{day.year}_{day.day}"
