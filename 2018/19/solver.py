from aoc import answer


@answer.timer
def main() -> None:
    answer.part1(993, factor_sum(961))
    answer.part2(10708912, factor_sum(10_551_361))


def factor_sum(value: int) -> int:
    result = 0
    for i in range(1, value + 1):
        if value % i == 0:
            result += i
    return result


if __name__ == "__main__":
    main()
