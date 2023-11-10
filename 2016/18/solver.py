from aoc import answer
from aoc.parser import Parser

TRAP, SAFE = "^", "."


def main() -> None:
    starting_row = Parser(strip=True).string()
    answer.part1(2013, total_safe(starting_row, 40))
    answer.part2(20006289, total_safe(starting_row, 400_000))


def total_safe(starting_row: str, n: int) -> int:
    previous_row = starting_row
    safe = count_safe(previous_row)
    for _ in range(n - 1):
        next_row = get_next_row(previous_row)
        previous_row = next_row
        safe += count_safe(next_row)
    return safe


def count_safe(row: str) -> int:
    return sum([element == SAFE for element in row])


def get_next_row(previous_row: str) -> str:
    next_row = []
    for i in range(len(previous_row)):
        element = get_element(
            previous_row[i - 1] if i > 0 else SAFE,
            previous_row[i + 1] if i < len(previous_row) - 1 else SAFE,
        )
        next_row.append(element)
    return "".join(next_row)


def get_element(left: str, right: str) -> str:
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
    return TRAP if left != right else SAFE


if __name__ == "__main__":
    main()
