from typing import Callable

from aoc import answer
from aoc.parser import Parser


@answer.timer
def main() -> None:
    jumps = Parser().int_lines()
    answer.part1(373160, run(jumps.copy(), lambda v: v + 1))
    answer.part2(26395586, run(jumps.copy(), lambda v: v - 1 if v >= 3 else v + 1))


def run(jumps: list[int], f: Callable[[int], int]) -> int:
    steps, ip = 0, 0
    while ip >= 0 and ip < len(jumps):
        jump = jumps[ip]
        jumps[ip] = f(jump)
        ip += jump
        steps += 1
    return steps


if __name__ == "__main__":
    main()
