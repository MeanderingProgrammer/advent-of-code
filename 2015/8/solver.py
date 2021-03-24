from collections import defaultdict

import aoc_search
from aoc_board import Grid, Point
from aoc_computer import Computer
from aoc_parser import Parser


TEST = False
FILE_NAME = 'sample' if TEST else 'data'


class String:

    def __init__(self, value):
        self.value = value

    def total(self):
        return len(self.value)

    def decode(self):
        result, i = [], 0
        while i < len(self.value):
            ch = self.value[i]
            if ch != '"':
                result.append(ch)
                if ch == '\\':
                    if self.value[i + 1] == 'x':
                        i += 3
                    else:
                        i += 1
            i += 1
        return len(result)

    def encode(self):
        result = ['"']
        for ch in self.value:
            if ch in ['\\', '"']:
                result.append('\\')
            result.append(ch)
        result.append('"')
        return len(result)



def main():
    total, decoded, encoded = [], [], []

    for line in Parser(FILE_NAME).lines():
        s = String(line)

        total.append(s.total())
        decoded.append(s.decode())
        encoded.append(s.encode())

    total, decoded, encoded = sum(total), sum(decoded), sum(encoded)

    # Part 1 = 1350
    print(total - decoded)
    # Part 2 = 2085
    print(encoded - total)


if __name__ == '__main__':
    main()

