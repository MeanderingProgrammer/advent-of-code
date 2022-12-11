from dataclasses import dataclass

@dataclass(order=True)
class Day:

    year: str
    day: str

    def next(self) -> 'Day':
        year, day = int(self.year), int(self.day)
        if day < 25:
            day += 1
        else:
            year += 1
            day = 1
        return Day(str(year), str(day).zfill(2))
