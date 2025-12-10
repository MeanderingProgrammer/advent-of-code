from dataclasses import dataclass
from typing import Self


@dataclass(frozen=True)
class Problems:
    ranges: list[tuple[int, int, int]]

    @classmethod
    def default(cls) -> Self:
        ranges = [
            # from 2015 (first year) until 2024 each year consisted of 25 problems
            (2015, 2024, 25),
            # starting in 2025 this was reduced to 12 problems.
            (2025, 2100, 12),
        ]
        return cls(ranges=ranges)

    @property
    def start(self) -> int:
        return self.ranges[0][0]

    @property
    def end(self) -> int:
        return self.ranges[-1][1]

    def get(self, year: int) -> int:
        for start, end, n in self.ranges:
            if start <= year <= end:
                return n
        raise Exception(f"year must be between {self.start} & {self.end}")
