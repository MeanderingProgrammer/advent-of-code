from dataclasses import dataclass
from typing import Self

from aoc import answer
from aoc.parser import Parser


@dataclass(frozen=True)
class DataRange:
    start: int
    end: int

    def can_join(self, o: Self) -> bool:
        if self.start <= o.start:
            return o.start <= self.end
        else:
            return o.end >= self.start

    def join(self, os: list[Self]) -> Self:
        data_ranges = os + [self]
        starts = [data_range.start for data_range in data_ranges]
        ends = [data_range.end for data_range in data_ranges]
        return type(self)(min(starts), max(ends))


def main() -> None:
    data_ranges = get_data_ranges()
    data_ranges = combine_all(data_ranges)
    data_ranges.sort(key=lambda data_range: data_range.start)

    answer.part1(17348574, data_ranges[0].end + 1)
    answer.part2(104, get_total_unblocked(data_ranges))


def get_data_ranges() -> list[DataRange]:
    data_ranges: list[DataRange] = []
    for line in Parser().lines():
        line = line.split("-")
        data_ranges.append(DataRange(int(line[0]), int(line[1])))
    return data_ranges


def combine_all(data_ranges: list[DataRange]) -> list[DataRange]:
    can_combine = True
    while can_combine:
        data_ranges, can_combine = combine(data_ranges)
    return data_ranges


def combine(data_ranges: list[DataRange]) -> tuple[list[DataRange], bool]:
    new_ranges: list[DataRange] = []
    joined: set[DataRange] = set()
    combined: bool = False
    for data_range in data_ranges:
        if data_range in joined:
            continue
        matches = get_matches(data_range, data_ranges)
        joined.add(data_range)
        for match in matches:
            joined.add(match)
        if len(matches) > 0:
            combined = True
            new_ranges.append(data_range.join(matches))
        else:
            new_ranges.append(data_range)
    return new_ranges, combined


def get_matches(data_range: DataRange, data_ranges: list[DataRange]) -> list[DataRange]:
    matches: list[DataRange] = []
    for other_range in data_ranges:
        if other_range != data_range and data_range.can_join(other_range):
            matches.append(other_range)
    return matches


def get_total_unblocked(data_ranges: list[DataRange]) -> int:
    return sum(
        [
            data_ranges[i].start - data_ranges[i - 1].end - 1
            for i in range(1, len(data_ranges))
        ]
    )


if __name__ == "__main__":
    main()
