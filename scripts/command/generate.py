import os
import shutil
from dataclasses import dataclass
from pathlib import Path
from typing import override

from command.command import Command
from language.language import Language
from pojo.day import Day


@dataclass(frozen=True)
class Generator(Command):
    day: Day
    language: Language
    puzzle: bool

    @override
    def info(self) -> dict:
        return dict(
            year=self.day.year,
            day=self.day.day,
            language=self.language.name,
            puzzle=self.puzzle,
        )

    @override
    def run(self) -> None:
        self.setup_solution()
        self.setup_data()

    def setup_solution(self) -> None:
        # Create day directory, okay if it already exists
        self.day.dir().mkdir(parents=True, exist_ok=True)
        # Copy over language template if not already present
        solution_path = self.language.solution_path(self.day)
        if solution_path.exists():
            print(f"Solution already exists under: {solution_path}")
            return
        self.copy_template()
        self.language.add_build(self.day)

    def copy_template(self) -> None:
        template_dir = Path(f"scripts/templates/{self.language.name}")
        if not template_dir.is_dir():
            raise Exception(f"No template defined in {template_dir}")
        for template_file in template_dir.glob("**/*"):
            if not template_file.is_file():
                continue
            file_path = template_file.relative_to(template_dir)
            destination = self.day.dir().joinpath(file_path)
            # Create parent directory if needed for nested solution files
            if not destination.parent.exists():
                destination.parent.mkdir(parents=True)
            if not destination.exists():
                print(f"Copying {template_file} to {destination}")
                shutil.copy(template_file, destination)

    def setup_data(self) -> None:
        # Create data directory, okay if it already exists
        data_dir = Path("data").joinpath(self.day.dir())
        data_dir.mkdir(parents=True, exist_ok=True)
        # Download the necessary files
        created = self.pull_aoc_file("-I -i", data_dir.joinpath("data.txt"))
        if created:
            Generator.empty_file(data_dir.joinpath("sample.txt"))
            push: list[str] = [
                "cd data",
                "git add .",
                f"git commit -m 'Add input for {self.day.dir()}'",
                "git push",
            ]
            os.system(" && ".join(push))
        if self.puzzle:
            self.pull_aoc_file("-P -p", data_dir.joinpath("puzzle.md"))

    def pull_aoc_file(self, flags: str, file: Path) -> bool:
        if file.exists():
            print(f"{file} already exists, leaving as is")
            return False
        print(f"Creating file at: {file}")
        cookie = ".adventofcode.session"
        if Path(cookie).exists() and shutil.which("aoc") is not None:
            print("Downloading input using aoc-cli")
            download: list[str] = [
                "aoc download",
                f"-y {self.day.year}",
                f"-d {self.day.day}",
                f"-s ./{cookie}",
                f"{flags} {file}",
            ]
            os.system(" ".join(download))
        else:
            print("aoc-cli is not setup")
            Generator.empty_file(file)
        return True

    @staticmethod
    def empty_file(file: Path) -> None:
        if not file.exists():
            print(f"Creating empty {file}")
            file.touch()
