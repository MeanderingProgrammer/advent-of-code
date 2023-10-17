import json
from pathlib import Path
from typing import List

from component.day_factory import DayFactory
from pojo.day import Day


class RunTemplate:
    def __init__(self):
        self.__templates = {
            "latest": RunTemplate.__latest,
            "previous": RunTemplate.__previous,
            "days": RunTemplate.__days,
            "languages": RunTemplate.__languages,
            "slow": RunTemplate.__slow,
        }

    def get_names(self) -> List[str]:
        return list(self.__templates.keys())

    def get(self, name) -> List[Day]:
        return self.__templates[name]()

    @staticmethod
    def __latest() -> List[Day]:
        return [DayFactory().get_latest()]

    @staticmethod
    def __previous() -> List[Day]:
        latest_day = DayFactory().get_latest()
        return [latest_day.add(-1)]

    @staticmethod
    def __days() -> List[Day]:
        return DayFactory([], []).get_days()

    @staticmethod
    def __languages() -> List[Day]:
        return [
            Day("2019", "01"),  # Python
            Day("2019", "20"),  # Java
            Day("2021", "01"),  # Rust & Go
        ]

    @staticmethod
    def __slow() -> List[Day]:
        slow_file = Path("slow.json")
        if not slow_file.is_file():
            raise Exception("Looks like slow runtimes were never determined")
        days = set()
        for runtime in json.loads(slow_file.read_text()):
            day = Day(runtime["year"], runtime["day"])
            days.add(day)
        return sorted(list(days))
