import json
from enum import StrEnum, auto
from pathlib import Path

from component.day_factory import DayFactory
from pojo.day import Day
from pojo.runtime_info import RuntimeInfo


class RunName(StrEnum):
    LATEST = auto()
    PREVIOUS = auto()
    ALL = auto()
    DAYS = auto()
    LANGUAGES = auto()
    SLOW = auto()


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

    @staticmethod
    def slow() -> list[Day]:
        slow_file = Path("slow.json")
        if not slow_file.is_file():
            raise Exception("Looks like slow runtimes were never determined")
        days = set()
        for runtime in json.loads(slow_file.read_text()):
            runtime_info = RuntimeInfo.from_dict(runtime)
            days.add(runtime_info.day)
        return sorted(list(days))
