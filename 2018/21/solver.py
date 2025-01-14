from aoc import answer


@answer.timer
def main() -> None:
    first, last = run()
    answer.part1(6619857, first)
    answer.part2(9547924, last)


def run() -> tuple[int, int]:
    seen: set[int] = set()
    current = run_inner(0)
    first, last = current, current
    while current not in seen:
        last = current
        seen.add(current)
        current = run_inner(current)
    return first, last


def run_inner(previous: int) -> int:
    # https://github.com/marcodelmastro/AdventOfCode2018/blob/master/Day%2021.ipynb
    counter = previous | 65536
    value = 9010242
    while counter > 0:
        value += counter & 255
        value &= 16777215
        value *= 65899
        value &= 16777215
        counter //= 256
    return value


if __name__ == "__main__":
    main()
