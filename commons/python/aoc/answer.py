def part1[T](expected: T, result: T) -> None:
    part(1, expected, result)


def part2[T](expected: T, result: T) -> None:
    part(2, expected, result)


def part[T](part: int, expected: T, result: T) -> None:
    if expected != result:
        raise Exception(f"Part {part} incorrect, expected {expected} but got {result}")
    print(f"Part {part}: {result}")
