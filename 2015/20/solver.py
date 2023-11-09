from aoc import answer
from aoc.parser import Parser


def main() -> None:
    goal = Parser().integer()
    answer.part1(665280, find_first(goal, False))
    answer.part2(705600, find_first(goal, True))


def find_first(goal: int, lazy: bool) -> int:
    max_value = goal // 10
    houses = [0] * max_value
    for i in range(1, max_value):
        elve_end = min((i * 50) + 1, max_value) if lazy else max_value
        multiplier = 11 if lazy else 10
        for house in range(i, elve_end, i):
            houses[house] += i * multiplier
    return first(goal, houses)


def first(goal: int, houses: list[int]) -> int:
    for i, house in enumerate(houses):
        if house >= goal:
            return i
    raise Exception("Should never get here")


if __name__ == "__main__":
    main()
