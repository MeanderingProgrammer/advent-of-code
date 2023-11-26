import json
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from component.figure_saver import FigureSaver


@dataclass(frozen=True)
class Grapher:
    archive: bool

    def graph(self) -> None:
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

        self.__create_graphs(runtimes, saver)

    def __create_graphs(self, runtimes: pd.DataFrame, saver: FigureSaver) -> None:
        saver.save(
            name="runtime_language",
            ax=runtimes.boxplot(column="runtime", by="language", figsize=(8, 8)),
        )
        saver.save(
            name="runtime_year",
            ax=runtimes.boxplot(column="runtime", by="year", figsize=(10, 8)),
        )

        yearly_runtimes = runtimes.groupby("year")["runtime"].sum()

        def format_label(pct: float) -> str:
            absolute = (pct / 100.0) * sum(yearly_runtimes)
            return f"{pct:.2f}%\n({absolute:.2f} seconds)"

        saver.save(
            name="year_percentage",
            ax=yearly_runtimes.plot.pie(
                autopct=format_label, colors=sns.color_palette("tab10"), figsize=(8, 8)
            ),
        )

        language_counts = runtimes["language"].value_counts()
        saver.save(
            name="usage_langauage",
            ax=language_counts.plot.pie(y=1, autopct="%.2f", figsize=(8, 6)),
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
            ax=yearly_usage.plot.bar(stacked=True, legend=False, figsize=(10, 6)),
            legend=dict(loc="upper center", ncol=5),
        )
