import pandas as pd
from termcolor import colored

from pojo.runtime_info import RuntimeInfo


class Displayer:
    def display(self, label: str, runtimes: list[RuntimeInfo]) -> None:
        if len(runtimes) == 0:
            print(f"{label}: NONE")
            return
        print(label)
        df = pd.DataFrame([runtime.as_dict() for runtime in runtimes])
        self._print_df(df)

    def _print_df(self, df) -> None:
        markdown = df.to_markdown(index=False)
        rows = markdown.split("\n")
        print("\n".join(rows[:2]))
        for i, row in enumerate(rows[2:]):
            print(colored(row, self._get_color(df.iloc[i])))

    @staticmethod
    def _get_color(row) -> str:
        color_predicates = {
            "green": lambda x: 0 <= x < 500,
            "yellow": lambda x: 500 <= x < 1_000,
            "red": lambda x: 1_000 <= x,
        }
        for color, predicate in color_predicates.items():
            if predicate(row["runtime"]):
                return color
        raise Exception(f"Could not find color for: {row}")
