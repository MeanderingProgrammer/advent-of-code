import json
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import override

import matplotlib.pyplot as plt
import pandas as pd
import plotly.express as px

from command.command import Command
from component.figure_saver import FigType, FigureSaver


@dataclass(frozen=True)
class Grapher(Command):
    archive: bool

    @override
    def info(self) -> dict:
        saver = self.__saver()
        return dict(
            archive=saver.archive, archive_directory=str(saver.archive_directory)
        )

    @override
    def run(self) -> None:
        plt.style.use("ggplot")

        runtimes_file = Path("all.json")
        if not runtimes_file.is_file():
            raise Exception(f"Runtimes were never determined: {runtimes_file}")
        runtimes = pd.DataFrame(json.loads(runtimes_file.read_text()))

        saver = self.__saver()
        if saver.archive_directory is not None:
            saver.archive_directory.mkdir(parents=True, exist_ok=False)

        runtimes["all"] = "ALL"
        runtimes["runtime"] = runtimes["runtime"].round(0)
        self.__create_graphs(runtimes, saver)

    def __saver(self) -> FigureSaver:
        archive_directory = None
        if self.archive:
            date_directory = datetime.now().strftime("%Y-%m-%d-%H-%M")
            archive_directory = Path("images/archive").joinpath(date_directory)
        return FigureSaver(archive=self.archive, archive_directory=archive_directory)

    def __create_graphs(self, runtimes: pd.DataFrame, saver: FigureSaver) -> None:
        saver.save(
            name="runtime_language",
            fig=runtimes.boxplot(column="runtime", by="language", figsize=(8, 8)),
            fig_type=FigType.MATPLOTLIB,
        )
        saver.save(
            name="runtime_year",
            fig=runtimes.boxplot(column="runtime", by="year", figsize=(10, 8)),
            fig_type=FigType.MATPLOTLIB,
        )

        yearly_runtimes = px.sunburst(
            runtimes,
            path=["all", "year", "day"],
            values="runtime",
            width=1000,
            height=1000,
        )
        yearly_runtimes.update_traces(textinfo="label+percent parent+value", sort=False)
        saver.save(
            name="year_percentage",
            fig=yearly_runtimes,
            fig_type=FigType.PLOTLY,
        )

        runtimes_only: pd.DataFrame = runtimes[["runtime"]]
        sorted_runtimes = runtimes_only.sort_values("runtime").reset_index(drop=True)
        saver.save(
            name="cumulative_sum",
            fig=sorted_runtimes.cumsum().plot.line(legend=False, figsize=(8, 6)),
            fig_type=FigType.MATPLOTLIB,
        )

        language_counts = runtimes["language"].value_counts()
        saver.save(
            name="usage_langauage",
            fig=language_counts.plot.pie(y=1, autopct="%.2f", figsize=(8, 6)),
            fig_type=FigType.MATPLOTLIB,
        )

        yearly_usage = pd.pivot_table(
            runtimes,
            index="year",
            columns="language",
            values="day",
            aggfunc="count",
            fill_value=0,
        )
        saver.save(
            name="usage_langauage_yearly",
            fig=yearly_usage.plot.bar(stacked=True, legend=False, figsize=(10, 6)),
            fig_type=FigType.MATPLOTLIB,
            legend=dict(loc="upper center", ncol=5),
        )
