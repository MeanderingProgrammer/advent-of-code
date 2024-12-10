import pytest

from aoc import answer


def test_correct() -> None:
    answer.part1(2, 2)
    answer.part2("abc", "abc")


def test_incorrect() -> None:
    with pytest.raises(Exception):
        answer.part1(2, -2)
