from dataclasses import dataclass
from enum import StrEnum, auto
from pathlib import Path
from typing import Any, ClassVar, Final

import matplotlib.pyplot as plt


class FigureKind(StrEnum):
    MATPLOTLIB = auto()
    PLOTLY = auto()


@dataclass(frozen=True)
class FigureProps:
    name: str
    figure: Any
    kind: FigureKind
    legend: dict[str, Any] | None = None


@dataclass(frozen=True)
class FigureSaver:
    ROOT: ClassVar[Final] = Path("images")

    archive: bool
    now: str

    def info(self) -> dict[str, Any]:
        return dict(
            archive=self.archive,
            now=self.now,
        )

    def save(self, props: FigureProps) -> None:
        """
        | archive | figure   | action          |
        | ------- | -------- | --------------- |
        | true    | existing | move to archive |
        | true    | new      | save in root    |
        | false   | existing | leave in root   |
        | false   | new      | save in archive |
        """

        file = f"{props.name}.png"
        root = FigureSaver.ROOT / file
        archive = FigureSaver.ROOT / "archive" / self.now / file
        assert not archive.exists()

        archive.parent.mkdir(parents=True, exist_ok=True)

        if self.archive:
            if root.exists():
                print(f"archiving {props.name}: {archive}")
                root.rename(archive)
            else:
                print(f"skip archiving {props.name}: missing")

        output = root if self.archive else archive
        print(f"saving {props.name}: {output}")
        assert not output.exists()

        fig, legend = props.figure, props.legend
        match props.kind:
            case FigureKind.MATPLOTLIB:
                if legend is not None:
                    fig.get_figure().legend(**legend)
                plt.tight_layout()
                fig.get_figure().savefig(str(output))
                fig.get_figure().clear()
            case FigureKind.PLOTLY:
                fig.write_image(file=str(output), format="png")
