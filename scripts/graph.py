import json
from pathlib import Path
from typing import Optional

import matplotlib.pyplot as plt
import pandas as pd


def main() -> None:
    plt.style.use("ggplot")

    runtimes_file = Path("all.json")
    if not runtimes_file.is_file():
        raise Exception(f"Looks like runtimes were never determined: {runtimes_file}")
    runtimes = pd.DataFrame(json.loads(runtimes_file.read_text()))

    save(
        name="runtime_language",
        ax=runtimes.boxplot(column="runtime", by="language", figsize=(8, 8)),
    )
    save(
        name="runtime_year",
        ax=runtimes.boxplot(column="runtime", by="year", figsize=(10, 8)),
    )

    language_counts = runtimes["language"].value_counts()
    save(
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
    save(
        name="usage_langauage_yearly",
        ax=yearly_usage.plot.bar(stacked=True, legend=False, figsize=(10, 6)),
        legend=dict(loc="upper center", ncol=5),
    )


def save(name: str, ax, legend: Optional[dict] = None) -> None:
    if legend is not None:
        ax.get_figure().legend(**legend)
    plt.tight_layout()
    ax.get_figure().savefig(f"images/{name}.png")
    ax.get_figure().clear()


if __name__ == "__main__":
    main()
