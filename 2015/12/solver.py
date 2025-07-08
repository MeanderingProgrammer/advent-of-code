import json

from aoc import answer
from aoc.parser import Parser

Doc = str | int | list["Doc"] | dict[str, "Doc"]


@answer.timer
def main() -> None:
    data = json.loads(Parser().string())
    answer.part1(111754, total(data, False))
    answer.part2(65402, total(data, True))


def total(value: Doc, ignore_red: bool) -> int:
    if isinstance(value, str):
        return 0
    elif isinstance(value, int):
        return value
    elif isinstance(value, list):
        return sum([total(entry, ignore_red) for entry in value])
    else:
        if ignore_red and "red" in value.values():
            return 0
        else:
            return sum([total(entry, ignore_red) for entry in value.values()])


if __name__ == "__main__":
    main()
