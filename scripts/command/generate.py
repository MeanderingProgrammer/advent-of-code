from dataclasses import dataclass
from datetime import datetime, timezone
from enum import StrEnum, auto
from pathlib import Path
from typing import Any

import requests

from component.command import Executor
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
        release = self.get_release_time()
        if current < release:
            print(f"problem will release in: {release - current}")
            return
        self.setup_solution()
        self.setup_data()

    def get_release_time(self) -> datetime:
        # problems release at 12:00AM EST / 5:00AM UTC
        year, day = int(self.day.year), int(self.day.day)
        return datetime(year, 12, day, 5, tzinfo=timezone.utc)

    def setup_solution(self) -> None:
        # create day directory, okay if it already exists
        self.day.dir().mkdir(parents=True, exist_ok=True)
        # copy over language template if not already present
        solution = self.day.dir() / self.language.file
        if solution.exists():
            print(f"solution already exists: {solution}")
            return
        self.setup_template()
        self.language.setup(self.day)

    def setup_template(self) -> None:
        root = Path(f"scripts/templates/{self.language.name}")
        assert root.is_dir(), f"no template defined: {root}"
        for file in root.rglob("*"):
            if not file.is_file():
                continue
            target = self.day.dir() / file.relative_to(root)
            # create parent directory if needed for nested solution files
            if not target.parent.exists():
                target.parent.mkdir(parents=True)
            if not target.exists():
                print(f"copying: {file} -> {target}")
                file.copy(target)

    def setup_data(self) -> None:
        repo = Path("data")

        # create data directory if it is missing
        root = repo / self.day.dir()
        root.mkdir(parents=True, exist_ok=True)

        data = root / "data.txt"
        sample = root / "sample.txt"
        match self.download_input(data):
            case Status.EXISTS:
                print(f"already exists: {data}")
            case Status.FAILED:
                Generator.create_empty(data)
                Generator.create_empty(sample)
            case Status.SUCCESS:
                Generator.create_empty(sample)
                Executor().call(["git", "add", "."], repo)
                Executor().call(
                    ["git", "commit", "-m", f"Add input for {self.day.dir()}"], repo
                )
                Executor().call(["git", "push"], repo)

    def download_input(self, path: Path) -> Status:
        if path.exists():
            return Status.EXISTS

        year, day = int(self.day.year), int(self.day.day)
        url = f"https://adventofcode.com/{year}/day/{day}/input"

        cookie = Path(".adventofcode.session")
        if not cookie.exists():
            print(f"missing session cookie: {cookie}")
            return Status.FAILED
        headers = dict(Cookie=f"session={cookie.read_text().strip()}")

        print(f"downloading input: {url}")
        response = requests.get(url, headers=headers)

        code = response.status_code
        if code != 200:
            print(f"request failed: {code}")
            return Status.FAILED

        print(f"writing data: {path}")
        path.write_text(response.text)
        return Status.SUCCESS

    @staticmethod
    def create_empty(path: Path) -> None:
        if not path.exists():
            print(f"creating empty: {path}")
            path.touch()
