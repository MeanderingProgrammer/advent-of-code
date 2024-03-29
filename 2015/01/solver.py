from aoc import answer
from aoc.parser import Parser


@answer.timer
def main() -> None:
    data = Parser().string()
    answer.part1(232, get_floor(data, False))
    answer.part2(1783, get_floor(data, True))


def get_floor(value: str, stop_at_basement: bool) -> int:
    floor = 0
    for i, ch in enumerate(value):
        if ch == "(":
            floor += 1
        else:
            floor -= 1
        if stop_at_basement and floor < 0:
            return i + 1
    return floor


if __name__ == "__main__":
    main()
