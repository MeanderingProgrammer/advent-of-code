from aoc import answer
from aoc.parser import Parser


@answer.timer
def main() -> None:
    values = Parser().lines()
    left, right = unzip_sort(values, 0), unzip_sort(values, 1)
    answer.part1(3246517, sum_diff(left, right))
    answer.part2(29379307, similarity(left, right))


def unzip_sort(values: list[str], i: int) -> list[int]:
    unzipped = [int(value.split()[i]) for value in values]
    unzipped.sort()
    return unzipped


def sum_diff(left: list[int], right: list[int]) -> int:
    return sum([abs(l - r) for l, r in zip(left, right)])


def similarity(left: list[int], right: list[int]) -> int:
    count: dict[int, int] = dict()
    for v in right:
        count[v] = count.get(v, 0) + 1
    return sum([v * count.get(v, 0) for v in left])


if __name__ == "__main__":
    main()
