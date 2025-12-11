from enum import StrEnum, auto

from component.day_factory import DayFactory
from pojo.day import Day


class GenerateName(StrEnum):
    NEXT = auto()
    CURRENT = auto()


class GenerateTemplate:
    def get(self, name: GenerateName) -> Day:
        match name:
            case GenerateName.NEXT:
                latest = DayFactory().get_latest()
                return latest.add(1)
            case GenerateName.CURRENT:
                return DayFactory().get_latest()
