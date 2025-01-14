from aoc import answer


@answer.timer
def main() -> None:
    answer.part1(993, factor_sum(961))
    answer.part2(10708912, factor_sum(10_551_361))


def factor_sum(value: int) -> int:
    factors: set[int] = set()
    for i in range(1, int(value**0.5) + 1):
        if value % i == 0:
            factors.add(i)
            factors.add(value // i)
    return sum(factors)


if __name__ == "__main__":
    main()
