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

    def build(self) -> list[list[str]]:
        return [
            ["cargo", "build", "-rq", "--bins"],
        ]

    def test(self) -> list[str]:
        return ["cargo", "test", "-rq", "--all-targets", "--", "--nocapture"]

    def run(self, day: Day, args: list[str]) -> list[str]:
        binary = Rust.binary(day)
        args = [] if len(args) == 0 else ["--"] + args
        return ["cargo", "run", "-rq", "--bin", binary] + args

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
    def binary(day: Day) -> str:
        return f"aoc_{day.year}_{day.day}"
