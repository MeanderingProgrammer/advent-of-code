from component.day_factory import DayFactory
from pojo.day import Day


class GenerateTemplate:

    def __init__(self):
        self.__template_mapping = {
            'next': GenerateTemplate.__get_next,
            'current': GenerateTemplate.__get_current,
        }

    def get(self, name) -> Day:
        valid_values = list(self.__template_mapping.keys())
        if name not in valid_values:
            raise Exception(f'Unknown template {name}, should be one of {valid_values}')
        return self.__template_mapping[name]()

    @staticmethod
    def __get_next() -> Day:
        latest_day = DayFactory().get_latest()
        return latest_day.add(1)

    @staticmethod
    def __get_current() -> Day:
        return DayFactory().get_latest()
