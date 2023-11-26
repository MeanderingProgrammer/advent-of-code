from dataclasses import dataclass
from pathlib import Path
from typing import Any, Optional

import matplotlib.pyplot as plt


@dataclass(frozen=True)
class FigureSaver:
    archive: bool
    archive_directory: Optional[Path]

    def save(self, name: str, ax: Any, legend: Optional[dict] = None) -> None:
        fig_path = Path(f"images/{name}.png")
        self.archive_figure(fig_path)
        if fig_path.exists():
            print(f"Skipping {fig_path} as it already exists")
        else:
            if legend is not None:
                ax.get_figure().legend(**legend)
            plt.tight_layout()
            ax.get_figure().savefig(str(fig_path))
        ax.get_figure().clear()

    def archive_figure(self, fig_path: Path) -> None:
        if not fig_path.exists() or not self.archive:
            return
        assert self.archive_directory is not None
        assert self.archive_directory.exists()
        fig_path.rename(self.archive_directory.joinpath(fig_path.name))
