from .point import Point, PointHelper

type Grid[T] = dict[Point, T]


class GridHelper:
    @staticmethod
    def xs[T](g: Grid[T]) -> set[int]:
        return set([point[0] for point in g])

    @staticmethod
    def ys[T](g: Grid[T]) -> set[int]:
        return set([point[1] for point in g])

    @staticmethod
    def rotate[T](g: Grid[T]) -> Grid[T]:
        result: Grid[T] = dict()
        for point, value in g.items():
            result[PointHelper.rotate(point)] = value
        return result

    @staticmethod
    def reflect[T](g: Grid[T]) -> Grid[T]:
        result: Grid[T] = dict()
        for point, value in g.items():
            result[PointHelper.reflect(point)] = value
        return result

    @staticmethod
    def mirror[T](g: Grid[T]) -> Grid[T]:
        result: Grid[T] = dict()
        for point, value in g.items():
            result[PointHelper.mirror(point)] = value
        return result

    @staticmethod
    def to_str[T](g: Grid[T]) -> str:
        rows: list[str] = []
        xs, ys = GridHelper.xs(g), GridHelper.ys(g)
        for y in range(max(ys), min(ys) - 1, -1):
            row: list[str] = []
            for x in range(min(xs), max(xs) + 1):
                row.append(str(g.get((x, y), ".")))
            rows.append("".join(row))
        return "\n".join(rows)
