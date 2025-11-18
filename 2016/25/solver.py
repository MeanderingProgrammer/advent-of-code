from aoc import answer
from aoc.assembunny import Computer
from aoc.parser import Parser


@answer.timer
def main() -> None:
    lines = Parser().lines()
    answer.part1(198, run(lines))


def run(lines: list[str]) -> int:
    i = 0
    success = False
    while not success:
        i += 1
        success = Computer.new(dict(a=i)).run(lines)
    return i


if __name__ == "__main__":
    main()
