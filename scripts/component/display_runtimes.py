from dataclasses import dataclass
from typing import Any, Literal

from pojo.day import Day
from pojo.runtime_info import RuntimeInfo


@dataclass(frozen=True)
class Color:
    min: float
    max: float
    value: int

    def contains(self, v: float) -> bool:
        return self.min <= v < self.max

    def wrap(self, s: str) -> str:
        return f"\033[{self.value}m{s}\033[0m"


@dataclass
class Column:
    name: str
    default: str | None
    width: int
    colors: list[Color]

    def __init__(self, name: str, default: str | None = None, *colors: Color) -> None:
        self.name = name
        self.default = default
        self.width = len(name)
        self.colors = list(colors)

    def get(self, runtime: dict[str, Any]) -> Any:
        value = runtime.get(self.name, self.default)
        assert value is not None
        return value

    def fit(self, runtime: dict[str, Any]) -> None:
        self.width = max(self.width, len(str(self.get(runtime))))

    def cell(self, s: Any) -> str:
        result = str(s).ljust(self.width)
        result = f" {result} "
        if isinstance(s, float):
            for color in self.colors:
                if color.contains(s):
                    result = color.wrap(result)
        return result


@dataclass
class Schema:
    columns: list[Column]

    def __init__(self, *columns: Column) -> None:
        self.columns = list(columns)

    def fit(self, runtime: dict[str, Any]) -> None:
        [column.fit(runtime) for column in self.columns]

    def delim(self, left: str, center: str, right: str) -> str:
        sections: list[str] = ["─" * (column.width + 2) for column in self.columns]
        return left + center.join(sections) + right

    def heading(self) -> str:
        return self.row([column.name for column in self.columns])

    def runtime(self, runtime: dict[str, Any]) -> str:
        return self.row([column.get(runtime) for column in self.columns])

    def row(self, values: list[Any]) -> str:
        line: list[str] = []
        for column, value in zip(self.columns, values):
            line.append(column.cell(value))
        return "│" + "│".join(line) + "│"


@dataclass(frozen=True)
class Displayer:
    label: Literal["all", "slow"]
    current: list[RuntimeInfo]
    previous: list[RuntimeInfo]

    def display(self) -> None:
        if len(self.current) == 0:
            print(f"{self.label.upper()}: NONE")
            return

        time: list[Color] = [
            Color(0, 500, 32),
            Color(500, 1000, 33),
            Color(1000, float("inf"), 31),
        ]
        change: list[Color] = [
            Color(float("-inf"), -10, 32),
            Color(10, float("inf"), 31),
        ]
        schema = Schema(
            Column("year"),
            Column("day"),
            Column("language"),
            Column("execution"),
            Column("runtime", None, *time),
            Column("previous", "none", *time),
            Column("delta", "none", *change),
        )

        previous_days: dict[Day, float] = dict()
        for runtime in self.previous:
            previous_days[runtime.day] = runtime.runtime

        runtimes: list[dict[str, Any]] = []
        for info in self.current:
            runtime = info.as_dict()
            previous = previous_days.get(info.day)
            if previous is not None:
                runtime["previous"] = round(previous, 3)
                runtime["delta"] = round(info.runtime - previous, 3)
            schema.fit(runtime)
            runtimes.append(runtime)

        print(self.label.upper())
        print(schema.delim("┌", "┬", "┐"))
        print(schema.heading())
        print(schema.delim("├", "┼", "┤"))
        [print(schema.runtime(runtime)) for runtime in runtimes]
        print(schema.delim("└", "┴", "┘"))
