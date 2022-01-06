import json

import commons.answer as answer
from commons.aoc_parser import Parser


class SantaData:

    def __init__(self, value, ignore_red):
        self.value = json.loads(value)
        self.ignore_red = ignore_red

    def total(self, value=None):
        value = self.value if value is None else value
        total = 0
        
        if isinstance(value, list):
            for entry in value:
                total += self.total(entry)
        elif isinstance(value, dict):
            if not self.ignore_red or not self.contains_red(value):
                for entry in value.values():
                    total += self.total(entry)
        elif isinstance(value, int):
            total += value
        elif isinstance(value, str):
            pass
        else:
            raise Exception('Unhandled: {}, Type: {}'.format(value, type(value)))

        return total

    @staticmethod
    def contains_red(value):
        return 'red' in value.values()


def main():
    answer.part1(111754, get_total(False))
    answer.part2(65402, get_total(True))


def get_total(ignore_red):
    santa = SantaData(Parser().string(), ignore_red)
    return santa.total()


if __name__ == '__main__':
    main()
