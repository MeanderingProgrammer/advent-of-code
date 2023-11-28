from dataclasses import dataclass
from enum import StrEnum
from typing import Optional, Self

from aoc import answer
from aoc.parser import Parser

Point = tuple[int, int]


def add(p1: Point, p2: Point) -> Point:
    return p1[0] + p2[0], p1[1] + p2[1]


DIRECTIONS: list[Point] = [
    (-1, 0),
    (-1, 1),
    (0, 1),
    (1, 1),
    (1, 0),
    (1, -1),
    (0, -1),
    (-1, -1),
]


class Seat(StrEnum):
    OCCUPIED = "#"
    EMPTY = "L"
    FLOOR = "."


@dataclass(frozen=True)
class SeatingChart:
    chart: dict[Point, Seat]
    look: bool

    def next(self) -> Self:
        next_chart = dict()
        for p, seat in self.chart.items():
            next_chart[p] = self.next_seat(p, seat)
        return type(self)(chart=next_chart, look=self.look)

    def next_seat(self, p: Point, seat: Seat) -> Seat:
        if seat == Seat.FLOOR:
            return seat
        elif seat == Seat.EMPTY:
            if self.adjacent_occupied(p) == 0:
                return Seat.OCCUPIED
            else:
                return seat
        elif seat == Seat.OCCUPIED:
            to_empty = 5 if self.look else 4
            if self.adjacent_occupied(p) >= to_empty:
                return Seat.EMPTY
            else:
                return seat
        else:
            raise Exception(f"Unexepected seat: {seat}")

    def adjacent_occupied(self, p: Point) -> int:
        result = 0
        for direction in DIRECTIONS:
            seat = self.explore_direction(p, direction)
            if seat == Seat.OCCUPIED:
                result += 1
        return result

    def explore_direction(self, p: Point, direction: Point) -> Optional[Seat]:
        point = add(p, direction)
        seat = self.chart.get(point)
        if not self.look:
            return seat
        while seat == Seat.FLOOR:
            point = add(point, direction)
            seat = self.chart.get(point)
        return seat

    def occupied(self) -> int:
        return sum([seat == Seat.OCCUPIED for seat in self.chart.values()])


def main() -> None:
    answer.part1(2386, run_until_stable(False))
    answer.part2(2091, run_until_stable(True))


def run_until_stable(look: bool) -> int:
    previous, current = None, get_chart(look)
    while previous != current:
        previous = current
        current = current.next()
    assert previous is not None
    return previous.occupied()


def get_chart(look: bool) -> SeatingChart:
    chart = dict()
    for y, row in enumerate(Parser().nested_lines()):
        for x, value in enumerate(row):
            chart[(x, y)] = Seat(value)
    return SeatingChart(chart=chart, look=look)


if __name__ == "__main__":
    main()
