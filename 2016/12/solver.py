from aoc import answer
from aoc.assembunny import Computer
from aoc.parser import Parser


@answer.timer
def main() -> None:
    lines = Parser().lines()
    answer.part1(318117, run(lines, 0))
    answer.part2(9227771, run(lines, 1))


def run(lines: list[str], c: int) -> int:
    computer = Computer.new(dict(c=c))
    assert computer.run(lines)
    return computer.get("a")


if __name__ == "__main__":
    main()
