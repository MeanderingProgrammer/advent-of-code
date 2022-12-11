from component.day_factory import DayFactory
from pojo.day import Day


class GenerateTemplate:

    def __init__(self):
        self.__template_mapping = {
            'next': GenerateTemplate.__get_next,
        }

    def get(self, name) -> Day:
        valid_values = list(self.__template_mapping.keys())
        if name not in valid_values:
            raise Exception(f'Unknown template {name}, should be one of {valid_values}')
        return self.__template_mapping[name]()

    @staticmethod
    def __get_next() -> Day:
        run_days = DayFactory([], []).get_days()
        run_days.sort(reverse=True)
        latest_day = run_days[0]
        return latest_day.next()
