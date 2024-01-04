import math

from aoc import answer
from aoc.computer import Computer
from aoc.parser import Parser


@answer.timer
def main() -> None:
    answer.part1(11662, run(7))
    # Ends up simplifying to n! + 77*86
    # Did some reverse engineering
    answer.part2(479008222, math.factorial(12) + 77 * 86)


def run(num_eggs: int) -> int:
    computer = Computer(registers=dict(a=num_eggs, b=0, c=0, d=0))
    computer.run(Parser().lines())
    return computer.get("a")


if __name__ == "__main__":
    main()
