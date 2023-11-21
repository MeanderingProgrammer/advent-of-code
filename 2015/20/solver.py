from aoc import answer
from aoc.parser import Parser


def main() -> None:
    goal = Parser().integer()
    answer.part1(665280, find_first(goal, False))
    answer.part2(705600, find_first(goal, True))


def find_first(goal: int, lazy: bool) -> int:
    houses: list[int] = [0] * (goal // 10)
    for i in range(1, len(houses)):
        last_house = (i * 50) + 1 if lazy else len(houses)
        for house in range(i, min(last_house, len(houses)), i):
            houses[house] += i * (11 if lazy else 10)
    return next(filter(lambda ih: ih[1] >= goal, enumerate(houses)))[0]


if __name__ == "__main__":
    main()
