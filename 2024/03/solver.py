import re

from aoc import answer
from aoc.parser import Parser


@answer.timer
def main() -> None:
    data = Parser().string()
    answer.part1(159892596, parse(data, False))
    answer.part2(92626942, parse(data, True))


def parse(data: str, toggle: bool) -> int:
    result: int = 0
    enabled: bool = True
    commands = re.findall(r"mul\(\d+,\d+\)|do\(\)|don't\(\)", data)
    for command in commands:
        if command.startswith("mul") and enabled:
            v1, v2 = command[4:-1].split(",")
            result += int(v1) * int(v2)
        elif command == "do()" and toggle:
            enabled = True
        elif command == "don't()" and toggle:
            enabled = False
    return result


if __name__ == "__main__":
    main()
