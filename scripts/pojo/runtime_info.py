from dataclasses import dataclass
from pojo.day import Day


@dataclass
class RuntimeInfo:
    day: Day
    language: str
    runtime: float

    def as_dict(self):
        return {
            "year": self.day.year,
            "day": self.day.day,
            "language": self.language,
            "runtime": self.runtime,
        }
