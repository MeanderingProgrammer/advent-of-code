import time
from functools import wraps
from typing import Callable


def timer(solution: Callable[[], None]) -> Callable[[], None]:
    @wraps(solution)
    def wrapper() -> None:
        start = time.time_ns()
        solution()
        end = time.time_ns()
        print(f"Runtime (ns): {end - start}")

    return wrapper


def part1[T](expected: T, actual: T) -> None:
    part(1, expected, actual)


def part2[T](expected: T, actual: T) -> None:
    part(2, expected, actual)


def part[T](part: int, expected: T, actual: T) -> None:
    if expected != actual:
        raise Exception(f"Part {part} incorrect, expected {expected} but got {actual}")
    print(f"Part {part}: {actual}")
