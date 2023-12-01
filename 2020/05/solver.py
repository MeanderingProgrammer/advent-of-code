from aoc import answer
from aoc.parser import Parser


class BoardingPass:
    def __init__(self, identifier: str):
        self.row = int(identifier[:7].replace("B", "1").replace("F", "0"), 2)
        self.seat = int(identifier[7:].replace("R", "1").replace("L", "0"), 2)

    def get_id(self) -> int:
        return (self.row * 8) + self.seat


def main() -> None:
    data = sorted(process())
    answer.part1(919, data[-1])
    binary = bin(find_missing(data))[2:]
    answer.part2(642, BoardingPass(binary).get_id())


def process() -> list[int]:
    return [BoardingPass(line).get_id() for line in Parser().lines()]


def find_missing(data: list[int]) -> int:
    for i, datum in enumerate(data):
        if datum - i != 80:
            return i + 80
    raise Exception("Failed")


if __name__ == "__main__":
    main()
