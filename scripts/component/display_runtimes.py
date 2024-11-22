from dataclasses import dataclass

from pojo.runtime_info import RuntimeInfo


@dataclass(frozen=True)
class Displayer:
    label: str
    runtimes: list[RuntimeInfo]

    def display(self) -> None:
        if len(self.runtimes) == 0:
            print(f"{self.label}: NONE")
            return

        headings: list[str] = ["year", "day", "language", "runtime", "execution"]

        rows: list[list[str]] = []
        for runtime in self.runtimes:
            info: dict = runtime.as_dict()
            row: list[str] = [str(info[name]) for name in headings]
            rows.append(row)

        widths: list[int] = [len(name) for name in headings]
        for row in rows:
            for i in range(len(headings)):
                widths[i] = max(widths[i], len(row[i]))

        print(self.label)
        Displayer.delim(widths, "┌", "┬", "┐")
        Displayer.row(widths, headings, None)
        Displayer.delim(widths, "├", "┼", "┤")
        for runtime, row in zip(self.runtimes, rows):
            Displayer.row(widths, row, runtime.runtime)
        Displayer.delim(widths, "└", "┴", "┘")

    @staticmethod
    def delim(widths: list[int], left: str, center: str, right: str) -> None:
        sections: list[str] = ["─" * (width + 2) for width in widths]
        print(left + center.join(sections) + right)

    @staticmethod
    def row(widths: list[int], cols: list[str], runtime: float | None) -> None:
        line: list[str] = []
        for col, width in zip(cols, widths):
            line.append(col.ljust(width))
        value = "│ " + " │ ".join(line) + " │"
        if runtime is None:
            print(value)
        else:
            color = Displayer.color(runtime)
            print(f"\033[{color}m{value}\033[0m")

    @staticmethod
    def color(value: float) -> int:
        if value < 500:
            return 32
        elif value < 1_000:
            return 33
        else:
            return 31
