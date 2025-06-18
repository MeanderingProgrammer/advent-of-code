from datetime import datetime
from typing import override

import matplotlib.pyplot as plt
import pandas as pd
import plotly.express as px

from command.command import Command
from component.figure_saver import FigureKind, FigureProps, FigureSaver
from component.history import History


class Grapher(Command):
    def __init__(self, archive: bool) -> None:
        self.saver = FigureSaver(
            archive=archive,
            now=datetime.now().strftime("%Y-%m-%d-%H-%M-%S"),
        )

    @override
    def info(self) -> dict:
        return self.saver.info()

    @override
    def run(self) -> None:
        plt.style.use("ggplot")
        runtimes = History("all").load(True)
        runtimes = pd.DataFrame([runtime.as_dict() for runtime in runtimes])
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
            figure=yearly_runtimes,
            kind=FigureKind.PLOTLY,
        )

    def runtime_language(self, runtimes: pd.DataFrame) -> FigureProps:
        return FigureProps(
            name="runtime_language",
            figure=runtimes.boxplot(
                column="runtime",
                by="language",
                figsize=(8, 8),
            ),
            kind=FigureKind.MATPLOTLIB,
        )

    def runtime_year(self, runtimes: pd.DataFrame) -> FigureProps:
        return FigureProps(
            name="runtime_year",
            figure=runtimes.boxplot(
                column="runtime",
                by="year",
                figsize=(10, 8),
            ),
            kind=FigureKind.MATPLOTLIB,
        )

    def cumulative_sum(self, runtimes: pd.DataFrame) -> FigureProps:
        runtimes_only: pd.DataFrame = runtimes[["runtime"]]  # type: ignore
        sorted_runtimes = runtimes_only.sort_values("runtime").reset_index(drop=True)
        return FigureProps(
            name="cumulative_sum",
            figure=sorted_runtimes.cumsum().plot.line(
                legend=False,
                figsize=(8, 6),
            ),
            kind=FigureKind.MATPLOTLIB,
        )

    def usage_langauage(self, runtimes: pd.DataFrame) -> FigureProps:
        language_counts = runtimes["language"].value_counts()
        return FigureProps(
            name="usage_langauage",
            figure=language_counts.plot.pie(
                y=1,
                autopct="%.2f",
                figsize=(8, 6),
            ),
            kind=FigureKind.MATPLOTLIB,
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
            figure=yearly_usage.plot.bar(
                stacked=True,
                legend=False,
                figsize=(10, 6),
            ),
            kind=FigureKind.MATPLOTLIB,
            legend=dict(loc="upper center", ncol=5),
        )

    def overhead(self, runtimes: pd.DataFrame) -> FigureProps:
        runtimes["overhead"] = runtimes["execution"] - runtimes["runtime"]
        return FigureProps(
            name="overhead_language",
            figure=runtimes.boxplot(
                column="overhead",
                by="language",
                figsize=(8, 8),
            ),
            kind=FigureKind.MATPLOTLIB,
        )
