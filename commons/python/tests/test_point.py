from aoc.point import Direction, Point, PointHelper


def test_math() -> None:
    assert (-3, 6) == PointHelper.add((1, 2), (-4, 4))
    assert (-5, -10) == PointHelper.multiply((1, 2), -5)


def test_movement() -> None:
    assert (1, 3) == PointHelper.go((1, 2), Direction.UP)


def test_neighbors() -> None:
    p: Point = (-1, 3)
    expected: list[Point] = [(-1, 2), (-1, 4), (0, 3), (-2, 3)]
    assert set(expected) == set(PointHelper.neighbors(p))


def test_all_neighbors() -> None:
    p: Point = (-1, 3)
    expected: list[Point] = [
        (-1, 2),
        (-1, 4),
        (0, 3),
        (-2, 3),
        (-2, 2),
        (-2, 4),
        (0, 2),
        (0, 4),
    ]
    assert set(expected) == set(PointHelper.all_neighbors(p))


def test_distance() -> None:
    assert 7 == PointHelper.distance((0, 0), (3, 4))
    assert 9 == PointHelper.len((-2, 7))
