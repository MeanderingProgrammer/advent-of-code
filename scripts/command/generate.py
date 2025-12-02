import os
import shutil
from dataclasses import dataclass
from datetime import datetime, timezone
from enum import StrEnum, auto
from pathlib import Path
from typing import Any

from language.language import Language
from pojo.day import Day


class Status(StrEnum):
    SUCCESS = auto()
    FAILED = auto()
    EXISTS = auto()


@dataclass(frozen=True)
class Generator:
    day: Day
    language: Language
    puzzle: bool

    def info(self) -> dict[str, Any]:
        return dict(
            year=self.day.year,
            day=self.day.day,
            language=self.language.name,
            puzzle=self.puzzle,
        )

    def run(self) -> None:
        current = datetime.now(timezone.utc)
        release = self.release_time()
        if current < release:
            minutes = (release - current).seconds // 60
            print("Problem not released yet")
            print(f"Check back in {minutes // 60} hours {minutes % 60} minutes")
        else:
            self.setup_solution()
            self.setup_data()

    def release_time(self) -> datetime:
        # Problems release at 12:00AM EST -> 5:00AM UTC
        year, day = int(self.day.year), int(self.day.day)
        return datetime(year, 12, day, 5, tzinfo=timezone.utc)

    def setup_solution(self) -> None:
        # Create day directory, okay if it already exists
        self.day.dir().mkdir(parents=True, exist_ok=True)
        # Copy over language template if not already present
        solution = self.day.file(self.language.file)
        if solution.exists():
            print(f"Solution already exists under: {solution}")
            return
        self.copy_template()
        self.language.setup(self.day)

    def copy_template(self) -> None:
        template_dir = Path(f"scripts/templates/{self.language.name}")
        if not template_dir.is_dir():
            raise Exception(f"No template defined in {template_dir}")
        for template_file in template_dir.glob("**/*"):
            if not template_file.is_file():
                continue
            file_path = template_file.relative_to(template_dir)
            destination = self.day.file(file_path)
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

        # Download data
        status = self.aoc_file("-I -i", data_dir.joinpath("data.txt"))
        if status != Status.EXISTS:
            Generator.empty_file(data_dir.joinpath("sample.txt"))
        if status == Status.SUCCESS:
            push: list[str] = [
                "cd data",
                "git add .",
                f"git commit -m 'Add input for {self.day.dir()}'",
                "git push",
            ]
            os.system(" && ".join(push))

        # Download puzzle
        if self.puzzle:
            self.aoc_file("-P -p", data_dir.joinpath("puzzle.md"))

    def aoc_file(self, flags: str, file: Path) -> Status:
        if file.exists():
            print(f"{file} already exists, leaving as is")
            return Status.EXISTS
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
            return Status.SUCCESS
        else:
            print("aoc-cli is not setup")
            Generator.empty_file(file)
            return Status.FAILED

    @staticmethod
    def empty_file(file: Path) -> None:
        if not file.exists():
            print(f"Creating empty {file}")
            file.touch()
