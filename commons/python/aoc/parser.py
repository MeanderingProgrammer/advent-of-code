import sys
from typing import List

from .board import Grid, Point


class Parser:
    def __init__(self, file_name="data"):
        self.file_name = "{}.txt".format(file_name)

    def string(self) -> str:
        file_path = "{}/{}".format(sys.path[0], self.file_name)
        with open(file_path, "r") as f:
            data = f.read()
        return data

    def ord_string(self) -> List[int]:
        return list(map(ord, self.string()))

    def entries(self) -> List[str]:
        return self.string().split()

    def int_entries(self) -> List[int]:
        return list(map(int, self.entries()))

    def csv(self) -> List[str]:
        data = self.string().split(",")
        return [datum.strip() for datum in data]

    def int_csv(self) -> List[int]:
        return list(map(int, self.csv()))

    def lines(self) -> List[str]:
        return self.string().split("\n")

    def int_lines(self) -> List[int]:
        return list(map(int, self.lines()))

    def nested_lines(self) -> List[List[str]]:
        return [[value for value in line] for line in self.lines()]

    def line_groups(self) -> List[List[str]]:
        return [group.split("\n") for group in self.string().split("\n\n")]

    def as_grid(self) -> Grid:
        """
        Grids are often created bottom up, where an increase in y leads a value that is
        up more. However files are read top down where an increased index means the value
        is lower in the file. Because I have found that directions being intuitive,
        i.e. up increases y and goes higher up on our grid I have chosen to create for
        line, offset, such that the last line in our file has y = 0. This is not typical as
        often in these scenarios you simply build a grid such that a higher y goes further
        down, but I dislike the directional semantics around that approach.
        """
        grid = Grid()
        lines = self.lines()
        max_y = len(lines) - 1
        for y, line in enumerate(lines):
            y = max_y - y
            for x, value in enumerate(line):
                point = Point(x, y)
                grid[point] = value
        return grid
