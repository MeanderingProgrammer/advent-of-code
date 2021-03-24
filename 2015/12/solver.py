import math
import json
import itertools
from collections import defaultdict

import aoc_search
from aoc_board import Grid, Point
from aoc_computer import Computer
from aoc_parser import Parser


TEST = False
FILE_NAME = 'sample' if TEST else 'data'


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
    # Part 1 = 111754
    get_total(False)
    # Part 2 = 65402
    get_total(True)


def get_total(ignore_red):
    for line in Parser(FILE_NAME).lines():
        data = SantaData(line, ignore_red)
        print(data.total())


if __name__ == '__main__':
    main()

