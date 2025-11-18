import argparse
import sys
from dataclasses import dataclass
from pathlib import Path

from .grid import Grid


@dataclass(frozen=True)
class AdventData:
    file_name: str | None = None

    def get_path(self) -> Path:
        year, day = sys.path[0].split("/")[-2:]
        file_name = self.file_name or self.get_name()
        return Path(f"data/{year}/{day}/{file_name}")

    def get_name(self) -> str:
        parser = argparse.ArgumentParser()
        parser.add_argument("--test", action="store_true")
        args = parser.parse_args()
        return "sample.txt" if args.test else "data.txt"


@dataclass(frozen=True)
class Parser:
    file_name: str | None = None
    data_file: bool = True

    def get_path(self) -> Path:
        if self.data_file:
            return AdventData(self.file_name).get_path()
        else:
            assert self.file_name is not None
            return Path(self.file_name)

    def string(self) -> str:
        return self.get_path().read_text().strip("\n")

    def integer(self) -> int:
        return int(self.string())

    def int_string(self) -> list[int]:
        return list(map(int, self.string()))

    def ord_string(self) -> list[int]:
        return list(map(ord, self.string()))

    def entries(self) -> list[str]:
        return self.string().split()

    def int_entries(self) -> list[int]:
        return list(map(int, self.entries()))

    def csv(self) -> list[str]:
        data = self.string().split(",")
        return [datum.strip() for datum in data]

    def int_csv(self) -> list[int]:
        return list(map(int, self.csv()))

    def lines(self) -> list[str]:
        return self.string().split("\n")

    def int_lines(self) -> list[int]:
        return list(map(int, self.lines()))

    def nested_lines(self) -> list[list[str]]:
        return [[value for value in line] for line in self.lines()]

    def line_groups(self) -> list[list[str]]:
        return [group.split("\n") for group in self.string().split("\n\n")]

    def grid(self) -> Grid[str]:
        """
        Grids are often created bottom up, where an increase in y leads a value that is
        up more. However files are read top down where an increased index means the value
        is lower in the file. Because I have found that directions being intuitive,
        i.e. up increases y and goes higher up on our grid I have chosen to create for
        line, offset, such that the last line in our file has y = 0. This is not typical as
        often in these scenarios you simply build a grid such that a higher y goes further
        down, but I dislike the directional semantics around that approach.
        """
        grid: Grid[str] = dict()
        lines = self.lines()
        max_y = len(lines) - 1
        for y, line in enumerate(lines):
            y = max_y - y
            for x, value in enumerate(line):
                grid[(x, y)] = value
        return grid
