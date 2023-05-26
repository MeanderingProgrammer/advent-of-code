import os

from dataclasses import dataclass, field
from pathlib import Path
from typing import List

from pojo.day import Day


@dataclass
class DayFactory:

    years: List[str] = field(default_factory=list)
    days: List[str] = field(default_factory=list)

    def get_latest(self) -> Day:
        days = self.get_days()
        days.sort(reverse=True)
        return days[0]

    def get_days(self) -> List[Day]:
        days = []
        for year in DayFactory._get_dirs_wth_prefix(self.years, '20'):
            os.chdir(year)
            for day in DayFactory._get_dirs_wth_prefix(self.days, None):
                days.append(Day(year, day))
            os.chdir('..')
        return sorted(days)
    
    @staticmethod
    def _get_dirs_wth_prefix(values: List[str], valid_prefix) -> List[str]:
        def path_predicate(file_path: Path) -> bool:
            # Must be a directory
            if not file_path.is_dir():
                return False

            dir_name = file_path.name
            # Name must match prefix if provided
            if valid_prefix is not None and not dir_name.startswith(valid_prefix):
                return False
            # Name must be in input values if provided
            if len(values) > 0 and not dir_name in values:
                return False
            # Passes all checks, should be a valid directory
            return True

        return [file_path.name for file_path in Path('.').iterdir() if path_predicate(file_path)]
