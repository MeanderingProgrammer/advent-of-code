from typing import Callable

from aoc import answer
from aoc.parser import Parser


@answer.timer
def main() -> None:
    answer.part1(373160, run(lambda v: v + 1))
    answer.part2(26395586, run(lambda v: v - 1 if v >= 3 else v + 1))


def run(f: Callable[[int], int]) -> int:
    jumps = Parser().int_lines()
    steps, ip = 0, 0
    while ip >= 0 and ip < len(jumps):
        jump = jumps[ip]
        jumps[ip] = f(jump)
        ip += jump
        steps += 1
    return steps


if __name__ == "__main__":
    main()
