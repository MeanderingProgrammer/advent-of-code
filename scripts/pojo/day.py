from dataclasses import dataclass

_START_YEAR = 2015
_PER_YEAR = 25


@dataclass(order=True)
class Day:

    year: str
    day: str

    def __post_init__(self):
        year, day = int(self.year), int(self.day)
        assert _START_YEAR <= year <= 2100, 'year must between 2015 & 2100'
        assert 1 <= day <= _PER_YEAR, 'day must be between 1 & 25'

    def add(self, amount: int) -> 'Day':
        value = self.__to_day_number()
        value += amount
        return Day.__from_day_number(value)

    def __to_day_number(self) -> int:
        year, day = int(self.year), int(self.day)
        year_number = year - _START_YEAR
        return year_number * _PER_YEAR + day

    @staticmethod
    def __from_day_number(value: int) -> 'Day':
        assert value > 0, 'Day number must be > 0'

        year_number = value // _PER_YEAR
        day_number = value % _PER_YEAR

        # Handle last day of year as special case
        if day_number == 0:
            year_number -= 1
            day_number = _PER_YEAR

        return Day(
            year=str(_START_YEAR + year_number),
            day=str(day_number).zfill(2),
        )
