use aoc_lib::answer;
use aoc_lib::grid::Grid;
use aoc_lib::point::{Direction, Point};
use aoc_lib::reader;

fn main() {
    let grid = reader::read_grid(|ch| Some(ch.to_digit(10).unwrap() as i64));
    let result: Vec<(i64, bool)> = grid
        .points()
        .iter()
        .map(|point| scenic_score(&grid, point))
        .collect();

    answer::part1(1533, result.iter().filter(|score| score.1).count());
    answer::part2(345744, result.iter().map(|score| score.0).max().unwrap());
}

fn scenic_score(grid: &Grid<i64>, point: &Point) -> (i64, bool) {
    let value = grid.get(point);
    let (v1, v1_edge) = distance_to_block(grid, point, value, &Direction::Right);
    let (v2, v2_edge) = distance_to_block(grid, point, value, &Direction::Left);
    let (v3, v3_edge) = distance_to_block(grid, point, value, &Direction::Down);
    let (v4, v4_edge) = distance_to_block(grid, point, value, &Direction::Up);
    (v1 * v2 * v3 * v4, v1_edge || v2_edge || v3_edge || v4_edge)
}

fn distance_to_block(
    grid: &Grid<i64>,
    point: &Point,
    value: &i64,
    direction: &Direction,
) -> (i64, bool) {
    let next_point = point.step(direction);
    if grid.contains(&next_point) {
        if grid.get(&next_point) >= value {
            (1, false)
        } else {
            let (child_dist, child_edge) = distance_to_block(grid, &next_point, value, direction);
            (1 + child_dist, child_edge)
        }
    } else {
        (0, true)
    }
}
