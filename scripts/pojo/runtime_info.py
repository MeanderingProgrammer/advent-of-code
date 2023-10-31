from dataclasses import dataclass

from pojo.day import Day


@dataclass(frozen=True)
class RuntimeInfo:
    day: Day
    language: str
    runtime: float

    def as_dict(self):
        return {
            "year": int(self.day.year),
            "day": int(self.day.day),
            "language": self.language,
            "runtime": self.runtime,
        }
