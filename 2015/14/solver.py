from dataclasses import dataclass
from typing import Self

from aoc import answer
from aoc.parser import Parser


@dataclass(frozen=True)
class Reindeer:
    speed: int
    time: int
    rest: int

    @classmethod
    def new(cls, s: str) -> Self:
        parts = s.split()
        return cls(
            speed=int(parts[3]),
            time=int(parts[6]),
            rest=int(parts[13]),
        )

    def distance(self, elapsed_time: int) -> int:
        complete, remainder = divmod(elapsed_time, self.time + self.rest)
        return self.speed * ((complete * self.time) + min(remainder, self.time))


@answer.timer
def main() -> None:
    reindeers = [Reindeer.new(line) for line in Parser().lines()]
    answer.part1(2655, max(distances_after(reindeers, 2_503)))
    answer.part2(1059, max_times_in_lead(reindeers, 2_503))


def distances_after(reindeers: list[Reindeer], time: int) -> list[int]:
    return [reindeer.distance(time) for reindeer in reindeers]


def max_times_in_lead(reindeers: list[Reindeer], time: int) -> int:
    times_in_lead: list[int] = [0] * len(reindeers)
    for seconds in range(1, time + 1):
        for index in maxes(distances_after(reindeers, seconds)):
            times_in_lead[index] += 1
    return max(times_in_lead)


def maxes(values: list[int]) -> list[int]:
    indexes: list[int] = []
    maximum_value = max(values)
    for i, value in enumerate(values):
        if value == maximum_value:
            indexes.append(i)
    return indexes


if __name__ == "__main__":
    main()
