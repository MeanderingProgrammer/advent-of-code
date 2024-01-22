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
        self.setup_language()
        self.setup_data_files()

    def setup_language(self) -> None:
        # Create day directory, okay if it already exists
        self.day.dir().mkdir(parents=True, exist_ok=True)
        # Copy over language template if not already present
        solution_path = self.language.solution_path(self.day)
        if solution_path.exists():
            print(f"Solution already exists under: {solution_path}")
        else:
            self.copy_template_files()
            self.language.template_processing(self.day)

    def copy_template_files(self) -> None:
        template_directory = Path(f"scripts/templates/{self.language.name}")
        if not template_directory.is_dir():
            raise Exception(f"No template defined in {template_directory}")
        for template_file in template_directory.glob("**/*"):
            if template_file.is_file():
                file_path = template_file.relative_to(template_directory)
                destination = self.day.dir().joinpath(file_path)
                # Create parent directory if needed for nested solution files
                if not destination.parent.exists():
                    destination.parent.mkdir(parents=True)
                if not destination.exists():
                    print(f"Copying {template_file} to {destination}")
                    shutil.copy(template_file, destination)

    def setup_data_files(self) -> None:
        # Create data directory, okay if it already exists
        data_dir = Path("data").joinpath(self.day.dir())
        data_dir.mkdir(parents=True, exist_ok=True)
        # Download the necessary files
        data_created = self.pull_aoc_file("-I -i", data_dir.joinpath("data.txt"))
        if data_created:
            Generator.create_empty_file(data_dir.joinpath("sample.txt"))
        if self.puzzle:
            self.pull_aoc_file("-P -p", data_dir.joinpath("puzzle.md"))

    def pull_aoc_file(self, flags: str, file_path: Path) -> bool:
        if file_path.exists():
            print(f"{file_path} already exists, leaving as is")
            return False
        print(f"Creating file at: {file_path}")
        advent_cookie_file = ".adventofcode.session"
        if Path(advent_cookie_file).exists() and shutil.which("aoc") is not None:
            print("Downloading input using aoc-cli")
            download_command = [
                "aoc download",
                f"-y {self.day.year}",
                f"-d {self.day.day}",
                f"-s ./{advent_cookie_file}",
                f"{flags} {file_path}",
            ]
            os.system(" ".join(download_command))
        else:
            print("aoc-cli is not setup")
            Generator.create_empty_file(file_path)
        return True

    @staticmethod
    def create_empty_file(file_path: Path) -> None:
        if not file_path.exists():
            print(f"Creating empty {file_path}")
            file_path.touch()
