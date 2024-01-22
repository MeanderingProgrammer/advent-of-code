from dataclasses import dataclass
from pathlib import Path
from typing import Final, Self

START_YEAR: Final[int] = 2015
PER_YEAR: Final[int] = 25


@dataclass(frozen=True, order=True)
class Day:
    year: str
    day: str

    def __post_init__(self):
        assert START_YEAR <= int(self.year) <= 2100, "year must be between 2015 & 2100"
        assert 1 <= int(self.day) <= PER_YEAR, "day must be between 1 & 25"

    def add(self, amount: int) -> Self:
        value = self.to_index() + amount
        assert value > 0, "Day number must be > 0"
        year, day = divmod(value, PER_YEAR)
        # Handle last day of year as special case
        if day == 0:
            year -= 1
            day = PER_YEAR
        return type(self)(
            year=str(START_YEAR + year),
            day=str(day).zfill(2),
        )

    def dir(self) -> Path:
        return Path(self.year).joinpath(self.day)

    def to_index(self) -> int:
        year = int(self.year) - START_YEAR
        return year * PER_YEAR + int(self.day)
