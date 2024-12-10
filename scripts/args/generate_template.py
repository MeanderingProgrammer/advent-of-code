from enum import StrEnum, auto

from component.day_factory import DayFactory
from pojo.day import Day


class GenerateName(StrEnum):
    NEXT = auto()
    CURRENT = auto()


class GenerateTemplate:
    def get(self, name: GenerateName) -> Day:
        if name == GenerateName.NEXT:
            latest_day = DayFactory().get_latest()
            return latest_day.add(1)
        elif name == GenerateName.CURRENT:
            return DayFactory().get_latest()
