from dataclasses import dataclass
from typing import Any

from pojo.day import Day


@dataclass(frozen=True)
class RuntimeInfo:
    day: Day
    language: str
    runtime: float
    execution: float

    def as_dict(self) -> dict[str, Any]:
        return dict(
            year=int(self.day.year),
            day=int(self.day.day),
            language=self.language,
            runtime=round(self.runtime, 3),
            execution=round(self.execution, 3),
        )

    @staticmethod
    def from_dict(value: dict) -> "RuntimeInfo":
        return RuntimeInfo(
            day=Day(
                year=str(value["year"]),
                day=str(value["day"]).zfill(2),
            ),
            language=value["language"],
            runtime=value["runtime"],
            execution=value["execution"],
        )
