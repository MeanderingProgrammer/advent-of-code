import os
import shutil
from dataclasses import dataclass
from pathlib import Path

from language.language import Language
from pojo.day import Day


@dataclass(frozen=True)
class Generator:
    day: Day
    language: Language
    puzzle: bool

    def run(self) -> None:
        # Create day directory, okay if it already exists
        self.day.dir().mkdir(parents=True, exist_ok=True)
        # Copy over language template if not already present
        solution_path = self.language.solution_path(self.day)
        if solution_path.exists():
            print(f"Solution already exists under: {solution_path}")
        else:
            self.__copy_template_files()
            self.language.template_processing(self.day)
        data_created = self.__pull_aoc_file("-I -i", "data.txt")
        if data_created:
            self.__create_sample_file()
        if self.puzzle:
            self.__pull_aoc_file("-P -p", "puzzle.md")

    def __copy_template_files(self) -> None:
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

    def __pull_aoc_file(self, flags: str, file_name: str) -> bool:
        file_path = self.day.dir().joinpath(file_name)
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
            print(f"Creating empty {file_path} since aoc-cli is not setup")
            file_path.touch()
        return True

    def __create_sample_file(self) -> None:
        sample_path = self.day.dir().joinpath("sample.txt")
        if not sample_path.exists():
            print(f"Creating empty {sample_path}")
            sample_path.touch()
