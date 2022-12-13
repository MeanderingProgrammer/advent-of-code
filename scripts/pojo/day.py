from dataclasses import dataclass

_START_YEAR = 2015
_PER_YEAR = 25


@dataclass(order=True)
class Day:

    year: str
    day: str

    def add(self, amount: int) -> 'Day':
        value = self.to_day_number()
        value += amount
        return Day.from_day_number(value)

    def to_day_number(self) -> int:
        year, day = int(self.year), int(self.day)
        assert _START_YEAR <= year <= 2100, 'year must between 2015 & 2100'
        assert 1 <= day <= _PER_YEAR, 'day must be between 1 & 25'

        year_number = year - _START_YEAR
        return year_number * 25 + day

    @staticmethod
    def from_day_number(value: int) -> 'Day':
        assert value > 0, 'Day number must be > 0'

        year_number = value // _PER_YEAR
        day_number = value % _PER_YEAR
        return Day(
            year=str(_START_YEAR + year_number),
            day=str(day_number).zfill(2),
        )
