import time
from typing import Callable


def timer(solution: Callable[[], None]) -> Callable[[], None]:
    def wrapper() -> None:
        start = time.time_ns()
        solution()
        end = time.time_ns()
        print(f"Runtime (ns): {end - start}")

    return wrapper


def part1[T](expected: T, result: T) -> None:
    part(1, expected, result)


def part2[T](expected: T, result: T) -> None:
    part(2, expected, result)


def part[T](part: int, expected: T, result: T) -> None:
    if expected != result:
        raise Exception(f"Part {part} incorrect, expected {expected} but got {result}")
    print(f"Part {part}: {result}")
