from aoc import answer
from aoc.parser import Parser


class BoardingPass:
    def __init__(self, identifier):
        row = identifier[:7]
        row = self.to_binary(row, "B")
        self.row = self.to_decimal(row)

        seat = identifier[7:]
        seat = self.to_binary(seat, "R")
        self.seat = self.to_decimal(seat)

    def get_id(self):
        return (self.row * 8) + self.seat

    @staticmethod
    def to_binary(value, high_value):
        result = []
        for char in value:
            if char == high_value:
                result.append(1)
            else:
                result.append(0)
        return result

    @staticmethod
    def to_decimal(binary):
        result = 0
        length = len(binary)
        for i, bit in enumerate(binary):
            exponent = length - i - 1
            converter = 2**exponent
            result += bit * converter
        return result


def main():
    data = process()
    data.sort()
    answer.part1(919, data[-1])

    code = to_code(to_binary(find_missing(data)), "BBBBBBBRRR", "FFFFFFFLLL")
    boarding_pass = BoardingPass(code)
    answer.part2(642, boarding_pass.get_id())


def find_missing(data):
    for i, datum in enumerate(data):
        diff = datum - i
        if diff != 80:
            return i + 80


def to_binary(value):
    result = []
    for i in range(10):
        exponent = 9 - i
        converter = 2**exponent
        if value >= converter:
            result.append(1)
            value -= converter
        else:
            result.append(0)
    return result


def to_code(binary, high_values, low_values):
    code = ""
    for i, bit in enumerate(binary):
        if bit == 1:
            code += high_values[i]
        else:
            code += low_values[i]
    return code


def process():
    return [BoardingPass(line).get_id() for line in Parser().lines()]


if __name__ == "__main__":
    main()
