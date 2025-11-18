import math

from aoc import answer
from aoc.assembunny import Computer
from aoc.parser import Parser


@answer.timer
def main() -> None:
    lines = Parser().lines()
    answer.part1(11662, run(lines, 7))
    # simplifies to n! + 77*86
    answer.part2(479008222, math.factorial(12) + 77 * 86)


def run(lines: list[str], a: int) -> int:
    computer = Computer.new(dict(a=a))
    assert computer.run(lines)
    return computer.get("a")


if __name__ == "__main__":
    main()
