import json
from argparse import ArgumentParser
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Optional

import matplotlib.pyplot as plt
import pandas as pd


@dataclass(frozen=True)
class FigureSaver:
    overwrite: bool

    def save(self, name: str, ax: Any, legend: Optional[dict] = None) -> None:
        fig_path = Path(f"images/{name}.png")
        if not self.overwrite and fig_path.exists():
            print(f"Skipping {fig_path} as it already exists")
        else:
            if legend is not None:
                ax.get_figure().legend(**legend)
            plt.tight_layout()
            ax.get_figure().savefig(str(fig_path))
        ax.get_figure().clear()


def main(overwrite: bool) -> None:
    plt.style.use("ggplot")

    runtimes_file = Path("all.json")
    if not runtimes_file.is_file():
        raise Exception(f"Looks like runtimes were never determined: {runtimes_file}")
    runtimes = pd.DataFrame(json.loads(runtimes_file.read_text()))

    saver = FigureSaver(overwrite=overwrite)

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
        ax=yearly_runtimes.plot.pie(autopct=format_label, figsize=(8, 8)),
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


if __name__ == "__main__":
    parser = ArgumentParser(description="Creates some fun graphs based on runtimes")
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Overwrite existing graphs with the same name",
    )
    args = parser.parse_args()
    main(args.overwrite)
