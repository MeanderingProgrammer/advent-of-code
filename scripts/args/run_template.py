from enum import StrEnum, auto
from pathlib import Path

from component.command import Executor
from component.day_factory import DayFactory
from component.history import History
from pojo.day import Day


class RunName(StrEnum):
    LATEST = auto()
    PREVIOUS = auto()
    ALL = auto()
    DAYS = auto()
    LANGUAGES = auto()
    SLOW = auto()
    CHANGED = auto()


class RunTemplate:
    def get(self, name: RunName) -> list[Day]:
        if name == RunName.LATEST:
            return [DayFactory().get_latest()]
        elif name == RunName.PREVIOUS:
            latest_day = DayFactory().get_latest()
            return [latest_day.add(-1)]
        elif name == RunName.ALL or name == RunName.DAYS:
            return DayFactory().get_days()
        elif name == RunName.LANGUAGES:
            # Single day implemented in all languages
            return [Day("2021", "01")]
        elif name == RunName.SLOW:
            return RunTemplate.slow()
        elif name == RunName.CHANGED:
            return RunTemplate.changed()

    @staticmethod
    def slow() -> list[Day]:
        days: set[Day] = set()
        for runtime in History("slow").load(True):
            days.add(runtime.day)
        return sorted(list(days))

    @staticmethod
    def changed() -> list[Day]:
        candidates: set[Path] = set()
        modified = Executor(False).run(["git", "diff", "--name-only", "--staged"])
        for line in modified.splitlines():
            path = Path(*Path(line).parts[:2])
            candidates.add(path)
        result: list[Day] = []
        for day in DayFactory().get_days():
            if day.dir() in candidates:
                result.append(day)
        return result
