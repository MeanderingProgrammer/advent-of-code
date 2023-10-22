import os
import shutil
from dataclasses import dataclass
from pathlib import Path

from language.language import Language
from pojo.day import Day

ADVENT_COOKIE_FILE = ".adventofcode.session"


@dataclass(frozen=True)
class Generator:
    day: Day
    language: Language

    def generate(self) -> None:
        date_path = self.__get_date_path()
        self.__check_solution_path(date_path)

        # At this point we can assume this is the first time we are processing
        # this day for this language, since the solution path does not exist
        self.__copy_template_to(date_path)
        self.language.template_processing(self.day)
        self.__create_sample_if_necessary(date_path)
        self.__create_data_if_necessary(date_path)

    def __get_date_path(self) -> Path:
        # Create date directory, okay if it already exists
        date_path = Path(self.day.year).joinpath(self.day.day)
        date_path.mkdir(parents=True, exist_ok=True)
        return date_path

    def __check_solution_path(self, date_path: Path) -> None:
        solution_path = date_path.joinpath(self.language.solution_file)
        if solution_path.exists():
            raise Exception(f"Solution already exists under: {solution_path}")

    def __copy_template_to(self, date_path: Path) -> None:
        template_directory = Path(f"scripts/templates/{self.language.name}")
        if not template_directory.is_dir():
            raise Exception(f"No template defined in {template_directory}")
        for template_file in template_directory.glob("**/*"):
            if template_file.is_file():
                file_path = template_file.relative_to(template_directory)
                destination = date_path.joinpath(file_path)
                # Create parent directory if needed for nested solution files
                if not destination.parent.exists():
                    destination.parent.mkdir(parents=True)
                if not destination.exists():
                    print(f"Copying {template_file} to {destination}")
                    os.system(f"cp {template_file} {destination}")

    def __create_sample_if_necessary(self, date_path: Path) -> None:
        sample_path = date_path.joinpath("sample.txt")
        if not sample_path.exists():
            print(f"Creating empty {sample_path}")
            sample_path.touch()

    def __create_data_if_necessary(self, date_path: Path) -> None:
        data_path = date_path.joinpath("data.txt")
        if not data_path.exists():
            print(f"Creating data file under: {data_path}")
            if Path(ADVENT_COOKIE_FILE).exists() and shutil.which("aoc") is not None:
                print("Downloading input using aoc-cli")
                self.__download_input(data_path)
            else:
                print(f"Creating empty {data_path} since aoc-cli is not setup")
                data_path.touch()
        else:
            print(f"{data_path} already exists, leaving as is")

    def __download_input(self, data_path: Path) -> None:
        download_command = [
            "aoc download",
            f"--year {self.day.year}",
            f"--day {self.day.day}",
            f"--input-file {data_path}",
            "--input-only",
            f"--session-file ./{ADVENT_COOKIE_FILE}",
        ]
        os.system(" ".join(download_command))
