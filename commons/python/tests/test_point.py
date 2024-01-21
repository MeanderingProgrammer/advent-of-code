from aoc.point import Point, PointHelper


def test_neighbors() -> None:
    p: Point = (-1, 3)
    assert set([(-1, 2), (-1, 4), (0, 3), (-2, 3)]) == set(PointHelper.neighbors(p))
