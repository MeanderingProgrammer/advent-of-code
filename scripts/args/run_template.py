import json
from pathlib import Path
from typing import Callable

from component.day_factory import DayFactory
from pojo.day import Day


class RunTemplate:
    def __init__(self):
        self.__templates: dict[str, Callable[[], list[Day]]] = {
            "latest": RunTemplate.__latest,
            "previous": RunTemplate.__previous,
            "days": RunTemplate.__days,
            "languages": RunTemplate.__languages,
            "slow": RunTemplate.__slow,
            "int-code": RunTemplate.__int_code,
        }

    def get_names(self) -> list[str]:
        return list(self.__templates.keys())

    def get(self, name: str) -> list[Day]:
        return self.__templates[name]()

    @staticmethod
    def __latest() -> list[Day]:
        return [DayFactory().get_latest()]

    @staticmethod
    def __previous() -> list[Day]:
        latest_day = DayFactory().get_latest()
        return [latest_day.add(-1)]

    @staticmethod
    def __days() -> list[Day]:
        return DayFactory().get_days()

    @staticmethod
    def __languages() -> list[Day]:
        # Single day implemented in all languages
        return [Day("2021", "01")]

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

    @staticmethod
    def __int_code() -> list[Day]:
        days = [2] + list(range(5, 26, 2))
        return DayFactory(years=[2019], days=days).get_days()
