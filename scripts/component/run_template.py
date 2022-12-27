from typing import List

from component.day_factory import DayFactory
from pojo.day import Day


class RunTemplate:

    def __init__(self):
        self.__template_mapping = {
            'latest': RunTemplate.__get_latest,
            'prev': RunTemplate.__get_previous,
            'all_days': RunTemplate.__get_all_days,
            'all_langs': RunTemplate.__get_all_languages,
        }

    def get(self, name) -> List[Day]:
        valid_values = list(self.__template_mapping.keys())
        if name not in valid_values:
            raise Exception(f'Unknown template {name}, should be one of {valid_values}')
        return self.__template_mapping[name]()

    @staticmethod
    def __get_latest() -> List[Day]:
        return [DayFactory().get_latest()]

    @staticmethod
    def __get_previous() -> List[Day]:
        latest_day = DayFactory().get_latest()
        return [latest_day.add(-1)]

    @staticmethod
    def __get_all_days() -> List[Day]:
        return DayFactory([], []).get_days()

    @staticmethod
    def __get_all_languages() -> List[Day]:
        return [
            Day('2019', '01'), # Python
            Day('2019', '20'), # Java
            Day('2021', '01'), # Rust & Go
        ]
