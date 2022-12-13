from typing import List, Tuple

from component.day_factory import DayFactory


class RunTemplate:

    def __init__(self):
        self.__template_mapping = {
            'latest': RunTemplate.__get_latest,
            'prev': RunTemplate.__get_previous,
            'all_days': RunTemplate.__get_all_days,
            'all_languages': RunTemplate.__get_all_languages,
        }

    def get(self, name) -> Tuple[List[str], List[str]]:
        valid_values = list(self.__template_mapping.keys())
        if name not in valid_values:
            raise Exception(f'Unknown template {name}, should be one of {valid_values}')
        return self.__template_mapping[name]()

    @staticmethod
    def __get_latest() -> Tuple[List[str], List[str]]:
        latest_day = DayFactory().get_latest()
        return (
            [latest_day.year],
            [latest_day.day],
        )
    
    @staticmethod
    def __get_previous() -> Tuple[List[str], List[str]]:
        latest_day = DayFactory().get_latest()
        previous_day = latest_day.add(-1)
        return (
            [previous_day.year],
            [previous_day.day],
        )
    
    @staticmethod
    def __get_all_days() -> Tuple[List[str], List[str]]:
        return (
            [],
            [],
        )

    @staticmethod
    def __get_all_languages() -> Tuple[List[str], List[str]]:
        # Python = 2019 - 01
        # Java = 2019 - 20
        # Rust & Go = 2021 - 01
        return (
            ['2019', '2021'],
            ['01', '20'],
        )
