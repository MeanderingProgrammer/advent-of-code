from dataclasses import dataclass
from typing import Optional

import pandas as pd

from pojo.runtime_info import RuntimeInfo


@dataclass(frozen=True)
class Color:
    value: int
    min: Optional[int] = None
    max: Optional[int] = None

    def matches(self, value: float) -> bool:
        if self.min is not None and value < self.min:
            return False
        if self.max is not None and value >= self.max:
            return False
        return True


class Displayer:
    def display(self, label: str, runtimes: list[RuntimeInfo]) -> None:
        if len(runtimes) == 0:
            print(f"{label}: NONE")
            return
        print(label)
        df = pd.DataFrame([runtime.as_dict() for runtime in runtimes])
        self.print_df(df)

    def print_df(self, df: pd.DataFrame) -> None:
        markdown = df.to_markdown(index=False)
        assert markdown is not None
        rows = markdown.split("\n")
        print("\n".join(rows[:2]))
        for i, row in enumerate(rows[2:]):
            color = Displayer.get_color(df.iloc[i])
            print(f"\033[{color}m{row}\033[0m")

    @staticmethod
    def get_color(row: dict) -> int:
        colors: list[Color] = [
            Color(value=32, max=500),
            Color(value=33, min=500, max=1_000),
            Color(value=31, min=1_000),
        ]
        for color in colors:
            if color.matches(row["runtime"]):
                return color.value
        raise Exception(f"Could not find color for: {row}")
