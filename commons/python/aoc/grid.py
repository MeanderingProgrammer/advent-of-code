from .point import Point, PointHelper

type Grid[T] = dict[Point, T]


class GridHelper:
    @staticmethod
    def xs(g: Grid) -> set[int]:
        return set([point[0] for point in g])

    @staticmethod
    def ys(g: Grid) -> set[int]:
        return set([point[1] for point in g])

    @staticmethod
    def rotate(g: Grid) -> Grid:
        result = dict()
        for point, value in g.items():
            result[PointHelper.rotate(point)] = value
        return result

    @staticmethod
    def reflect(g: Grid) -> Grid:
        result = dict()
        for point, value in g.items():
            result[PointHelper.reflect(point)] = value
        return result

    @staticmethod
    def mirror(g: Grid) -> Grid:
        result = dict()
        for point, value in g.items():
            result[PointHelper.mirror(point)] = value
        return result

    @staticmethod
    def to_str(g: Grid) -> str:
        rows: list[str] = []
        xs, ys = GridHelper.xs(g), GridHelper.ys(g)
        for y in range(max(ys), min(ys) - 1, -1):
            row: list[str] = []
            for x in range(min(xs), max(xs) + 1):
                row.append(str(g.get((x, y), ".")))
            rows.append("".join(row))
        return "\n".join(rows)
