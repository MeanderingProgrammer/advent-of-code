from typing import List

from component.day_factory import DayFactory
from pojo.day import Day


class GenerateTemplate:
    def __init__(self):
        self.__templates = {
            "next": GenerateTemplate.__next,
            "current": GenerateTemplate.__current,
        }

    def get_names(self) -> List[str]:
        return list(self.__templates.keys())

    def get(self, name) -> Day:
        return self.__templates[name]()

    @staticmethod
    def __next() -> Day:
        latest_day = DayFactory().get_latest()
        return latest_day.add(1)

    @staticmethod
    def __current() -> Day:
        return DayFactory().get_latest()
