import re
from dataclasses import dataclass

from aoc import answer
from aoc.parser import Parser

Point = tuple[int, int]


@dataclass(frozen=True)
class Claim:
    claim_id: int
    point: Point
    width: int
    height: int

    def get_points(self) -> list[Point]:
        points: list[Point] = []
        for x in range(self.width):
            for y in range(self.height):
                points.append((self.point[0] + x, self.point[1] + y))
        return points


@answer.timer
def main() -> None:
    grid: dict[Point, list[int]] = get_overlap_grid()

    all_claims: set[int] = set()
    multiple_claims: set[int] = set()
    multiple_claim_points: int = 0
    for claim_ids in grid.values():
        all_claims.update(claim_ids)
        if len(claim_ids) > 1:
            multiple_claims.update(claim_ids)
            multiple_claim_points += 1

    answer.part1(120408, multiple_claim_points)
    answer.part2(1276, next(iter(all_claims.difference(multiple_claims))))


def get_overlap_grid() -> dict[Point, list[int]]:
    grid: dict[Point, list[int]] = dict()
    for claim in get_claims():
        for point in claim.get_points():
            if point not in grid:
                grid[point] = []
            grid[point].append(claim.claim_id)
    return grid


def get_claims() -> list[Claim]:
    claim_pattern = "^#(.*) @ (.*),(.*): (.*)x(.*)$"
    claims: list[Claim] = []
    for line in Parser().lines():
        match = re.match(claim_pattern, line)
        assert match is not None
        claim = Claim(
            claim_id=int(match[1]),
            point=(int(match[2]), int(match[3])),
            width=int(match[4]),
            height=int(match[5]),
        )
        claims.append(claim)
    return claims


if __name__ == "__main__":
    main()
