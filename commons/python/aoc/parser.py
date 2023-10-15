import sys
from typing import List
from .board import Point, Grid


class Parser:
    def __init__(self, file_name="data"):
        self.file_name = "{}.txt".format(file_name)

    def string(self):
        return self.__read(split=False)

    def ord_string(self):
        return self.__to_ord(self.string())

    def entries(self):
        return self.__read()

    def int_entries(self):
        return self.__to_int(self.entries())

    def csv(self):
        return self.__read(sep=",", strip=True)

    def int_csv(self):
        return self.__to_int(self.csv())

    def lines(self) -> List[str]:
        return self.__read(sep="\n")

    def int_lines(self):
        return self.__to_int(self.lines())

    def nested_lines(self) -> List[List[str]]:
        return [[value for value in line] for line in self.lines()]

    def line_groups(self):
        return [group.split("\n") for group in self.__read(sep="\n\n")]

    def as_grid(self):
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

    def __read(self, split=True, sep=None, strip=False):
        file_path = "{}/{}".format(sys.path[0], self.file_name)
        with open(file_path, "r") as f:
            data = f.read()
        if split:
            data = data.split(sep)
            if strip:
                data = [datum.strip() for datum in data]
        return data

    def __to_int(self, values):
        return self.__map(values, int)

    def __to_ord(self, values):
        return self.__map(values, ord)

    @staticmethod
    def __map(values, f):
        return [f(value) for value in values]
