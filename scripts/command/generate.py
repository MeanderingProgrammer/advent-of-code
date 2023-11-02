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

    def generate(self) -> None:
        # Create day directory, okay if it already exists
        self.day.dir().mkdir(parents=True, exist_ok=True)
        solution_path = self.day.dir().joinpath(self.language.solution_file)
        if solution_path.exists():
            raise Exception(f"Solution already exists under: {solution_path}")

        # At this point we can assume this is the first time we are processing
        # this day for this language, since the solution path does not exist
        self.__copy_template_files()
        self.language.template_processing(self.day)
        self.__create_sample()
        self.__create_data()

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
                    os.system(f"cp {template_file} {destination}")

    def __create_sample(self) -> None:
        sample_path = self.day.dir().joinpath("sample.txt")
        if not sample_path.exists():
            print(f"Creating empty {sample_path}")
            sample_path.touch()

    def __create_data(self) -> None:
        data_path = self.day.dir().joinpath("data.txt")
        if data_path.exists():
            print(f"{data_path} already exists, leaving as is")
            return

        print(f"Creating data file at: {data_path}")
        advent_cookie_file = ".adventofcode.session"
        if Path(advent_cookie_file).exists() and shutil.which("aoc") is not None:
            print("Downloading input using aoc-cli")
            download_command = [
                "aoc download",
                f"--year {self.day.year}",
                f"--day {self.day.day}",
                f"--input-file {data_path}",
                "--input-only",
                f"--session-file ./{advent_cookie_file}",
            ]
            os.system(" ".join(download_command))
        else:
            print(f"Creating empty {data_path} since aoc-cli is not setup")
            data_path.touch()
