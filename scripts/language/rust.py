from dataclasses import dataclass
from pathlib import Path

import tomlkit
from tomlkit.items import AoT

from pojo.day import Day


@dataclass(frozen=True)
class Rust:
    name: str = "rust"
    file: str = "solver.rs"
    cmd: str = "cargo"

    def test(self) -> list[str]:
        return Rust.cargo("test") + ["--test", "aoc"]

    def build(self) -> list[list[str]]:
        return [Rust.cargo("build") + ["--bins"]]

    def run(self, day: Day, args: list[str]) -> list[str]:
        args = [] if len(args) == 0 else ["--"] + args
        return Rust.cargo("run") + ["--bin", Rust.binary(day)] + args

    def setup(self, day: Day) -> None:
        config = tomlkit.table()
        config["name"] = Rust.binary(day)
        config["path"] = str(day.file(self.file))

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
