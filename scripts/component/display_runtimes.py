import pandas as pd
from termcolor import colored
from typing import List
from pojo.runtime_info import RuntimeInfo


class Displayer:
    def __init__(self, runtimes: List[RuntimeInfo]):
        self.__df = pd.DataFrame([runtime.as_dict() for runtime in runtimes])

    def display(self):
        self._print_df("ALL", self.__df)
        self._print_df("SLOW", self.__df[self.__df["runtime"] > 10])

    def _print_df(self, label, df):
        if df.shape[0] == 0:
            print("{}: NONE".format(label))
            return

        print(label)
        markdown = df.to_markdown(index=False)
        rows = markdown.split("\n")
        print("\n".join(rows[:2]))
        for i, row in enumerate(rows[2:]):
            print(colored(row, self._get_color(df.iloc[i])))

    @staticmethod
    def _get_color(row):
        color_predicates = {
            "green": lambda x: 0 <= x < 0.5,
            "yellow": lambda x: 0.5 <= x < 10,
            "red": lambda x: 10 <= x,
        }
        for color, predicate in color_predicates.items():
            if predicate(row["runtime"]):
                return color
