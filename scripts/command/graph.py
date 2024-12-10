import json
from datetime import datetime
from pathlib import Path
from typing import override

import matplotlib.pyplot as plt
import pandas as pd
import plotly.express as px
from command.command import Command
from component.figure_saver import FigType, FigureProps, FigureSaver


class Grapher(Command):

    def __init__(self, archive: bool) -> None:
        archive_directory = None
        if archive:
            date_directory = datetime.now().strftime("%Y-%m-%d-%H-%M")
            archive_directory = Path("images/archive").joinpath(date_directory)
        self.saver = FigureSaver(
            archive=archive,
            archive_directory=archive_directory,
        )

    @override
    def info(self) -> dict:
        return dict(
            archive=self.saver.archive,
            archive_directory=str(self.saver.archive_directory),
        )

    @override
    def run(self) -> None:
        plt.style.use("ggplot")

        runtimes_file = Path("all.json")
        if not runtimes_file.is_file():
            raise Exception(f"Runtimes were never determined: {runtimes_file}")
        runtimes = pd.DataFrame(json.loads(runtimes_file.read_text()))

        if self.saver.archive_directory is not None:
            self.saver.archive_directory.mkdir(parents=True, exist_ok=False)

        self.create_graphs(runtimes)

    def create_graphs(self, runtimes: pd.DataFrame) -> None:
        self.saver.save(self.year_percentage(runtimes.copy()))
        self.saver.save(self.runtime_language(runtimes.copy()))
        self.saver.save(self.runtime_year(runtimes.copy()))
        self.saver.save(self.cumulative_sum(runtimes.copy()))
        self.saver.save(self.usage_langauage(runtimes.copy()))
        self.saver.save(self.usage_langauage_yearly(runtimes.copy()))
        self.saver.save(self.overhead(runtimes.copy()))

    def year_percentage(self, runtimes: pd.DataFrame) -> FigureProps:
        runtimes["all"] = "Time in milliseconds"
        runtimes["runtime"] = runtimes["runtime"].round(0)
        yearly_runtimes = px.sunburst(
            runtimes,
            path=["all", "year", "day"],
            values="runtime",
            width=1000,
            height=1000,
        )
        yearly_runtimes.update_traces(
            textinfo="label+percent parent+value",
            sort=False,
        )
        return FigureProps(
            name="year_percentage",
            fig=yearly_runtimes,
            fig_type=FigType.PLOTLY,
        )

    def runtime_language(self, runtimes: pd.DataFrame) -> FigureProps:
        return FigureProps(
            name="runtime_language",
            fig=runtimes.boxplot(
                column="runtime",
                by="language",
                figsize=(8, 8),
            ),
            fig_type=FigType.MATPLOTLIB,
        )

    def runtime_year(self, runtimes: pd.DataFrame) -> FigureProps:
        return FigureProps(
            name="runtime_year",
            fig=runtimes.boxplot(
                column="runtime",
                by="year",
                figsize=(10, 8),
            ),
            fig_type=FigType.MATPLOTLIB,
        )

    def cumulative_sum(self, runtimes: pd.DataFrame) -> FigureProps:
        runtimes_only: pd.DataFrame = runtimes[["runtime"]]
        sorted_runtimes = runtimes_only.sort_values("runtime").reset_index(drop=True)
        return FigureProps(
            name="cumulative_sum",
            fig=sorted_runtimes.cumsum().plot.line(
                legend=False,
                figsize=(8, 6),
            ),
            fig_type=FigType.MATPLOTLIB,
        )

    def usage_langauage(self, runtimes: pd.DataFrame) -> FigureProps:
        language_counts = runtimes["language"].value_counts()
        return FigureProps(
            name="usage_langauage",
            fig=language_counts.plot.pie(
                y=1,
                autopct="%.2f",
                figsize=(8, 6),
            ),
            fig_type=FigType.MATPLOTLIB,
        )

    def usage_langauage_yearly(self, runtimes: pd.DataFrame) -> FigureProps:
        yearly_usage = pd.pivot_table(
            runtimes,
            index="year",
            columns="language",
            values="day",
            aggfunc="count",
            fill_value=0,
        )
        return FigureProps(
            name="usage_langauage_yearly",
            fig=yearly_usage.plot.bar(
                stacked=True,
                legend=False,
                figsize=(10, 6),
            ),
            fig_type=FigType.MATPLOTLIB,
            legend=dict(loc="upper center", ncol=5),
        )

    def overhead(self, runtimes: pd.DataFrame) -> FigureProps:
        runtimes["overhead"] = runtimes["execution"] - runtimes["runtime"]
        return FigureProps(
            name="overhead_language",
            fig=runtimes.boxplot(
                column="overhead",
                by="language",
                figsize=(8, 8),
            ),
            fig_type=FigType.MATPLOTLIB,
        )
