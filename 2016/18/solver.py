from aoc import answer
from aoc.parser import Parser


def main() -> None:
    starting_row = [v == "." for v in Parser(strip=True).string()]
    answer.part1(2013, total_safe(starting_row, 40))
    answer.part2(20006289, total_safe(starting_row, 400_000))


def total_safe(starting_row: list[bool], n: int) -> int:
    safe = 0
    row = list(starting_row)
    for _ in range(n):
        safe += sum(row)
        row = next_row(row)
    return safe


def next_row(row: list[bool]) -> list[bool]:
    result = []
    for i in range(len(row)):
        element = get_element(
            row[i - 1] if i > 0 else True,
            row[i + 1] if i < len(row) - 1 else True,
        )
        result.append(element)
    return result


def get_element(left: bool, right: bool) -> bool:
    """
    Raw conditions for a TRAP can be summed up as an or of:
    1)  L &  C & ~R
    2) ~L &  C &  R
    3)  L & ~C & ~R
    4) ~L & ~C &  R

    Doing some simple grouping we learn that the center value plays no role:
    (L & C & ~R) | (L & ~C & ~R) -> L & (C | ~C) & ~R -> L & ~R
    (~L & C & R) | (~L & ~C & R) -> ~L & (C | ~C) & R -> ~L & R

    Further simplifies to an exclusive or, i.e. not equal (one true one false)
    (L & ~R) | (~L & R) -> L ^ R
    """
    return left == right


if __name__ == "__main__":
    main()
