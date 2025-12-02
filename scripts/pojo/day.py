from dataclasses import dataclass, field
from pathlib import Path
from typing import Final, Self


@dataclass(frozen=True)
class Problems:
    ranges: list[tuple[int, int, int]] = field(default_factory=list)

    def __post_init__(self) -> None:
        # from 2015 (first year) until 2024 each year consisted of 25 problems
        self.ranges.append((2015, 2024, 25))
        # starting in 2025 this was reduced to 12 problems.
        self.ranges.append((2025, 2100, 12))

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


PROBLEMS: Final[Problems] = Problems()


@dataclass(frozen=True, order=True)
class Day:
    year: str
    day: str

    def __post_init__(self) -> None:
        problems = PROBLEMS.get(int(self.year))
        assert 1 <= int(self.day) <= problems, f"day must be between 1 & {problems}"

    def add(self, amount: int) -> Self:
        index = self.index() + amount
        assert index > 0, "index must be > 0"
        year = PROBLEMS.start
        while True:
            problems = PROBLEMS.get(year)
            if index <= problems:
                break
            index -= problems
            year += 1
        return type(self)(
            year=str(year),
            day=str(index).zfill(2),
        )

    def index(self) -> int:
        result = 0
        for year in range(PROBLEMS.start, int(self.year)):
            result += PROBLEMS.get(year)
        return result + int(self.day)

    def dir(self) -> Path:
        return Path(self.year).joinpath(self.day)

    def file(self, name: Path | str) -> Path:
        return self.dir().joinpath(name)
