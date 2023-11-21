from typing import Callable

from component.day_factory import DayFactory
from pojo.day import Day


class GenerateTemplate:
    def __init__(self):
        self.__templates: dict[str, Callable[[], Day]] = {
            "next": GenerateTemplate.__next,
            "current": GenerateTemplate.__current,
        }

    def get_names(self) -> list[str]:
        return list(self.__templates.keys())

    def get(self, name: str) -> Day:
        return self.__templates[name]()

    @staticmethod
    def __next() -> Day:
        latest_day = DayFactory().get_latest()
        return latest_day.add(1)

    @staticmethod
    def __current() -> Day:
        return DayFactory().get_latest()
