from aoc import answer
from aoc.parser import Parser


def main():
    data = Parser().string()
    print(data)
    answer.part1(1, 1)


if __name__ == "__main__":
    main()
