from collections import defaultdict

import aoc_search
from aoc_parser import Parser
from aoc_board import Grid, Point


TEST = False
FILE_NAME = 'sample' if TEST else 'data'


class Scanner:

    def __init__(self, value):
        parts = value.split(': ')
        self.layer = int(parts[0])
        self.layer_range = int(parts[1])
        self.roundtrip = (self.layer_range - 1) * 2

    def caught(self, offset=0):
        return (self.layer + offset) % self.roundtrip == 0

    def severity(self):
        return self.layer * self.layer_range


def main():
    scanners = get_scanners()

    # Part 1 = 632
    print('Trip severity = {}'.format(get_trip_severity(scanners)))

    # Part 2 = 3849742
    offset = 1
    while is_caught(scanners, offset):
        offset += 1
    print('Offset needed = {}'.format(offset))


def get_trip_severity(scanners):
    severities = []
    for scanner in scanners:
        if scanner.caught():
            severities.append(scanner.severity())
    return sum(severities)


def is_caught(scanners, offset):
    for scanner in scanners:
        if scanner.caught(offset):
            return True
    return False


def get_scanners():
    scanners = []
    for line in Parser(FILE_NAME).lines():
        scanners.append(Scanner(line))
    return scanners


if __name__ == '__main__':
    main()

