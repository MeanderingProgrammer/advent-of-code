from dataclasses import dataclass, field
from pathlib import Path

from pojo.day import Day


class Everything:
    def __contains__(self, _) -> bool:
        return True


@dataclass(frozen=True)
class DayFactory:
    years: list[int] = field(default_factory=list)
    days: list[int] = field(default_factory=list)

    def get_latest(self) -> Day:
        days = self.get_days()
        days.sort(reverse=True)
        return days[0]

    def get_days(self) -> list[Day]:
        valid_years = self.__valid_years()
        valid_days = self.__valid_days()

        days = []
        for solution_directory in Path(".").glob("2*/*"):
            year, day = solution_directory.parts
            if year in valid_years and day in valid_days:
                days.append(Day(year, day))
        return sorted(days)

    def __valid_years(self):
        years = [str(year if year > 2_000 else year + 2_000) for year in self.years]
        return years if len(years) > 0 else Everything()

    def __valid_days(self):
        days = [str(day).zfill(2) for day in self.days]
        return days if len(days) > 0 else Everything()
