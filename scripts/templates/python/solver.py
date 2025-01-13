from aoc import answer
from aoc.parser import Parser


@answer.timer
def main() -> None:
    data = Parser().string()
    print(data)
    answer.part1(1, 1)
    answer.part2(1, 1)


if __name__ == "__main__":
    main()
