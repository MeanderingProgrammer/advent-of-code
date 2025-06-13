from dataclasses import dataclass
from pathlib import Path
from typing import override

import tomlkit
from language.language import Language
from pojo.day import Day
from tomlkit.items import AoT


@dataclass
class Rust(Language):

    @property
    @override
    def name(self) -> str:
        return "rust"

    @property
    @override
    def file(self) -> str:
        return "solver.rs"

    @property
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
    def run_command(self, day: Day, args: list[str]) -> list[str]:
        args = [] if len(args) == 0 else ["--"] + args
        return Rust.cargo("run") + ["--bin", Rust.binary(day)] + args

    @override
    def add_build(self, day: Day) -> None:
        config = tomlkit.table()
        config["name"] = Rust.binary(day)
        config["path"] = str(day.dir().joinpath(self.file))

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
