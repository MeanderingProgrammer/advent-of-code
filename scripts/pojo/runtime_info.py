from dataclasses import dataclass

from pojo.day import Day


@dataclass(frozen=True)
class RuntimeInfo:
    day: Day
    language: str
    runtime: float

    def as_dict(self) -> dict:
        return {
            "year": int(self.day.year),
            "day": int(self.day.day),
            "language": self.language,
            "runtime": self.runtime,
        }

    @staticmethod
    def from_dict(value: dict) -> "RuntimeInfo":
        return RuntimeInfo(
            day=Day(
                year=str(value["year"]),
                day=str(value["day"]).zfill(2),
            ),
            language=value["language"],
            runtime=value["runtime"],
        )
