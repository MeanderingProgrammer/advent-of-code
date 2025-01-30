from dataclasses import dataclass
from enum import StrEnum, auto
from pathlib import Path
from typing import Any, Optional

import matplotlib.pyplot as plt


class FigureKind(StrEnum):
    MATPLOTLIB = auto()
    PLOTLY = auto()


@dataclass(frozen=True)
class FigureProps:
    name: str
    figure: Any
    kind: FigureKind
    legend: Optional[dict] = None


@dataclass(frozen=True)
class FigureSaver:
    archive: bool
    now: str

    def info(self) -> dict:
        return dict(
            archive=self.archive,
            now=self.now,
        )

    def save(self, props: FigureProps) -> None:
        """
        archive: existing figure -> archive directory
                 new figure -> root directory
        else   : existing figure -> stay in root directory
                 new figure -> archive directory
        """

        root_dir = Path("images")
        archive_dir = root_dir.joinpath("archive").joinpath(self.now)
        archive_dir.mkdir(parents=True, exist_ok=True)

        name = f"{props.name}.png"
        root_path = root_dir.joinpath(name)
        archive_path = archive_dir.joinpath(name)

        if self.archive:
            if root_path.exists():
                print(f"Moving {props.name} from {root_path} to {archive_path}")
                assert not archive_path.exists()
                root_path.rename(archive_path)
            else:
                print(f"Skip archiving {props.name}, {root_path} already empty")

        path = root_path if self.archive else archive_path
        print(f"Saving {props.name} to {path}")
        assert not path.exists()

        if props.kind == FigureKind.MATPLOTLIB:
            self.save_matplotlib(props.figure, props.legend, path)
        elif props.kind == FigureKind.PLOTLY:
            self.save_plotly(props.figure, path)
        else:
            raise Exception(f"Unhandled figure kind: {props.kind}")

    def save_matplotlib(self, fig: Any, legend: Optional[dict], path: Path) -> None:
        if legend is not None:
            fig.get_figure().legend(**legend)
        plt.tight_layout()
        fig.get_figure().savefig(str(path))
        fig.get_figure().clear()

    def save_plotly(self, fig: Any, path: Path) -> None:
        fig.write_image(file=str(path), format="png")
