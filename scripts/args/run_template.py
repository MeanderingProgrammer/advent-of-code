import json
from enum import StrEnum, auto
from pathlib import Path

from component.day_factory import DayFactory
from pojo.day import Day


class RunName(StrEnum):
    LATEST = auto()
    PREVIOUS = auto()
    ALL = auto()
    DAYS = auto()
    LANGUAGES = auto()
    INT_CODE = auto()
    SLOW = auto()


class RunTemplate:
    def get_names(self) -> list[str]:
        return [run_name.value for run_name in RunName]

    def get(self, name: str) -> list[Day]:
        run_name = RunName(name)
        if run_name == RunName.LATEST:
            return [DayFactory().get_latest()]
        elif run_name == RunName.PREVIOUS:
            latest_day = DayFactory().get_latest()
            return [latest_day.add(-1)]
        elif run_name in [RunName.ALL, RunName.DAYS]:
            return DayFactory().get_days()
        elif run_name == RunName.LANGUAGES:
            # Single day implemented in all languages
            return [Day("2021", "01")]
        elif run_name == RunName.INT_CODE:
            days = [2] + list(range(5, 26, 2))
            return DayFactory(years=[2019], days=days).get_days()
        elif run_name == RunName.SLOW:
            return RunTemplate.__slow()
        else:
            raise Exception(f"Unhandled name: {run_name}")

    @staticmethod
    def __slow() -> list[Day]:
        slow_file = Path("slow.json")
        if not slow_file.is_file():
            raise Exception("Looks like slow runtimes were never determined")
        days = set()
        for runtime in json.loads(slow_file.read_text()):
            day_factory = DayFactory(years=[runtime["year"]], days=[runtime["day"]])
            days.update(day_factory.get_days())
        return sorted(list(days))
