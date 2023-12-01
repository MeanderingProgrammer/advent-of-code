from aoc import answer


def main() -> None:
    halt_values = run()
    answer.part1(6619857, halt_values[0])
    answer.part2(9547924, halt_values[-1])


def run() -> list[int]:
    seen: list[int] = []
    current = run_inner(0)
    while current not in seen:
        seen.append(current)
        current = run_inner(current)
    return seen


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
