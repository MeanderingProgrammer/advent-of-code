from enum import StrEnum, auto

from component.day_factory import DayFactory
from pojo.day import Day


class GenerateName(StrEnum):
    NEXT = auto()
    CURRENT = auto()


class GenerateTemplate:
    def get_names(self) -> list[str]:
        return [generate_name.value for generate_name in GenerateName]

    def get(self, name: str) -> Day:
        generate_name = GenerateName(name)
        if generate_name == GenerateName.NEXT:
            latest_day = DayFactory().get_latest()
            return latest_day.add(1)
        elif generate_name == GenerateName.CURRENT:
            return DayFactory().get_latest()
        else:
            raise Exception(f"Unhandled name: {generate_name}")
