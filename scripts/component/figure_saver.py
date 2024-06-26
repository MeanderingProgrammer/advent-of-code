from dataclasses import dataclass
from enum import StrEnum, auto
from pathlib import Path
from typing import Any, Optional

import matplotlib.pyplot as plt


class FigType(StrEnum):
    MATPLOTLIB = auto()
    PLOTLY = auto()


@dataclass(frozen=True)
class FigureProps:
    name: str
    fig: Any
    fig_type: FigType
    legend: Optional[dict] = None


@dataclass(frozen=True)
class FigureSaver:
    archive: bool
    archive_directory: Optional[Path]

    def save(self, props: FigureProps) -> None:
        fig_path = Path(f"images/{props.name}.png")
        self.archive_figure(fig_path)

        if fig_path.exists():
            print(f"Skipping {fig_path} as it already exists")
        else:
            print(f"Creating {fig_path}")
            if props.fig_type == FigType.MATPLOTLIB:
                self.save_matplotlib(props.fig, props.legend, fig_path)
            elif props.fig_type == FigType.PLOTLY:
                self.save_plotly(props.fig, fig_path)
            else:
                raise Exception(f"Unhandled figure type: {props.fig_type}")

        if props.fig_type == FigType.MATPLOTLIB:
            props.fig.get_figure().clear()

    def archive_figure(self, fig_path: Path) -> None:
        if not fig_path.exists() or not self.archive:
            return
        assert self.archive_directory is not None
        assert self.archive_directory.exists()
        fig_path.rename(self.archive_directory.joinpath(fig_path.name))

    def save_matplotlib(self, fig: Any, legend: Optional[dict], fig_path: Path) -> None:
        if legend is not None:
            fig.get_figure().legend(**legend)
        plt.tight_layout()
        fig.get_figure().savefig(str(fig_path))

    def save_plotly(self, fig: Any, fig_path: Path) -> None:
        fig.write_image(file=str(fig_path), format="png")
