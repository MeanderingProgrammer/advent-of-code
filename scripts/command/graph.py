import json
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import plotly.express as px
from component.figure_saver import FigType, FigureSaver


@dataclass(frozen=True)
class Grapher:
    archive: bool

    def run(self) -> None:
        plt.style.use("ggplot")

        runtimes_file = Path("all.json")
        if not runtimes_file.is_file():
            raise Exception(f"Runtimes were never determined: {runtimes_file}")
        runtimes = pd.DataFrame(json.loads(runtimes_file.read_text()))

        archive_directory = None
        if self.archive:
            date_directory = datetime.now().strftime("%Y-%m-%d-%H-%M")
            archive_directory = Path("images/archive").joinpath(date_directory)
            archive_directory.mkdir(parents=True, exist_ok=False)
        saver = FigureSaver(archive=self.archive, archive_directory=archive_directory)

        runtimes["all"] = "ALL"
        runtimes["runtime"] = runtimes["runtime"].round(3)
        self.__create_graphs(runtimes, saver)

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
