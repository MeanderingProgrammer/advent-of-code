import json
from typing import Any

from aoc import answer
from aoc.parser import Parser


@answer.timer
def main() -> None:
    answer.part1(111754, get_total(False))
    answer.part2(65402, get_total(True))


def get_total(ignore_red: bool) -> int:
    return total(json.loads(Parser().string()), ignore_red)


def total(value: Any, ignore_red: bool) -> int:
    result = 0
    if isinstance(value, list):
        result += sum([total(entry, ignore_red) for entry in value])
    elif isinstance(value, dict):
        if not ignore_red or "red" not in value.values():
            result += sum([total(entry, ignore_red) for entry in value.values()])
    elif isinstance(value, int):
        result += value
    elif isinstance(value, str):
        result += 0
    else:
        raise Exception(f"Unhandled: {value}, Type: {type(value)}")
    return result


if __name__ == "__main__":
    main()
