import os
from typing import List, override

import toml
from language.language import Language
from pojo.day import Day

_CARGO_FILE = "Cargo.toml"


class Rust(Language):
    @property
    @override
    def name(self) -> str:
        return "rust"

    @property
    @override
    def solution_file(self) -> str:
        return "solver.rs"

    @override
    def _run_setup(self) -> None:
        os.system("cargo build -rq --bins")

    @override
    def compile(self) -> None:
        # Since our setup command builds all binary targets, each day does not
        # need to be individually compiled
        pass

    @override
    def _get_run_command(self, day: Day, run_args: List[str]) -> List[str]:
        args = [] if len(run_args) == 0 else ["--"] + run_args
        return ["cargo", "run", "-rq", "--bin", Rust.__binary(day)] + args

    @override
    def template_processing(self, day: Day) -> None:
        cargo = toml.load(_CARGO_FILE)
        bin_config = {
            "name": Rust.__binary(day),
            "path": f"{day.year}/{day.day}/{self.solution_file}",
        }
        if bin_config in cargo["bin"]:
            print("Do not need to update Cargo file")
            return

        cargo["bin"].append(bin_config)
        cargo["bin"].sort(key=lambda bin: bin["name"])
        Rust.__save_cargo_file(cargo)

    @staticmethod
    def __binary(day: Day) -> str:
        return f"aoc_{day.year}_{day.day}"

    @staticmethod
    def __save_cargo_file(cargo) -> None:
        f = open(_CARGO_FILE, "w+")
        f.write(toml.dumps(cargo))
        f.close()
