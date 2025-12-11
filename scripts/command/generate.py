import os
import shutil
from dataclasses import dataclass
from datetime import datetime, timezone
from enum import StrEnum, auto
from pathlib import Path
from typing import Any

import requests

from language.language import Language
from pojo.day import Day


class Status(StrEnum):
    EXISTS = auto()
    FAILED = auto()
    SUCCESS = auto()


@dataclass(frozen=True)
class Generator:
    day: Day
    language: Language

    def info(self) -> dict[str, Any]:
        return dict(
            year=self.day.year,
            day=self.day.day,
            language=self.language.name,
        )

    def run(self) -> None:
        current = datetime.now(timezone.utc)
        release = self.release_time()
        if current < release:
            minutes = (release - current).seconds // 60
            print("problem not released yet")
            print(f"check back in {minutes // 60} hours {minutes % 60} minutes")
        else:
            self.setup_solution()
            self.setup_data()

    def release_time(self) -> datetime:
        # problems release at 12:00AM EST / 5:00AM UTC
        year, day = int(self.day.year), int(self.day.day)
        return datetime(year, 12, day, 5, tzinfo=timezone.utc)

    def setup_solution(self) -> None:
        # create day directory, okay if it already exists
        self.day.dir().mkdir(parents=True, exist_ok=True)
        # copy over language template if not already present
        solution = self.day.file(self.language.file)
        if solution.exists():
            print(f"solution already exists under: {solution}")
            return
        self.copy_template()
        self.language.setup(self.day)

    def copy_template(self) -> None:
        directory = Path(f"scripts/templates/{self.language.name}")
        if not directory.is_dir():
            raise Exception(f"no template defined in: {directory}")
        for file in directory.glob("**/*"):
            if not file.is_file():
                continue
            path = file.relative_to(directory)
            destination = self.day.file(path)
            # create parent directory if needed for nested solution files
            if not destination.parent.exists():
                destination.parent.mkdir(parents=True)
            if not destination.exists():
                print(f"copying {file} to {destination}")
                shutil.copy(file, destination)

    def setup_data(self) -> None:
        # create data directory, okay if it already exists
        directory = Path("data").joinpath(self.day.dir())
        directory.mkdir(parents=True, exist_ok=True)

        data = directory.joinpath("data.txt")
        sample = directory.joinpath("sample.txt")
        match self.download(data):
            case Status.EXISTS:
                print(f"already exists: {data}")
            case Status.FAILED:
                Generator.empty_file(data)
                Generator.empty_file(sample)
            case Status.SUCCESS:
                Generator.empty_file(sample)
                push: list[str] = [
                    "cd data",
                    "git add .",
                    f"git commit -m 'Add input for {self.day.dir()}'",
                    "git push",
                ]
                os.system(" && ".join(push))

    def download(self, file: Path) -> Status:
        if file.exists():
            return Status.EXISTS

        cookie = Path(".adventofcode.session")
        if not cookie.exists():
            print(f"missing session cookie: {cookie}")
            return Status.FAILED

        url = f"https://adventofcode.com/{self.day.year}/day/{int(self.day.day)}/input"
        headers = dict(
            Cookie=f"session={cookie.read_text().strip()}",
        )
        print(f"downloading input: {url}")
        response = requests.get(url, headers=headers)
        code = response.status_code
        if code != 200:
            print(f"request failed: {code}")
            return Status.FAILED

        print(f"writing data: {file}")
        file.write_text(response.text)
        return Status.SUCCESS

    @staticmethod
    def empty_file(file: Path) -> None:
        if not file.exists():
            print(f"creating empty: {file}")
            file.touch()
