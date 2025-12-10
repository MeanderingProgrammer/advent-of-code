from dataclasses import dataclass
from pathlib import Path
from typing import ClassVar, Final, Self

from pojo.problems import Problems


@dataclass(frozen=True, order=True)
class Day:
    PROBLEMS: ClassVar[Final[Problems]] = Problems.default()

    year: str
    day: str

    def __post_init__(self) -> None:
        problems = Day.PROBLEMS.get(int(self.year))
        assert 1 <= int(self.day) <= problems, f"day must be between 1 & {problems}"

    def add(self, amount: int) -> Self:
        index = self.index() + amount
        assert index > 0, "index must be > 0"
        year = Day.PROBLEMS.start
        while True:
            problems = Day.PROBLEMS.get(year)
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
        for year in range(Day.PROBLEMS.start, int(self.year)):
            result += Day.PROBLEMS.get(year)
        return result + int(self.day)

    def dir(self) -> Path:
        return Path(self.year).joinpath(self.day)

    def file(self, name: Path | str) -> Path:
        return self.dir().joinpath(name)
