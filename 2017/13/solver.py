import commons.answer as answer
from commons.aoc_parser import Parser


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

    answer.part1(632, get_trip_severity(scanners))
    
    offset = 1
    while is_caught(scanners, offset):
        offset += 1
    answer.part2(3849742, offset)


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
    return [Scanner(line) for line in Parser().lines()]


if __name__ == '__main__':
    main()
