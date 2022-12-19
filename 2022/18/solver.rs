use aoc_lib::answer;
use aoc_lib::grid::Grid;
use aoc_lib::point::Point;
use aoc_lib::reader;
use queues::{IsQueue, Queue};
use std::collections::HashSet;

fn main() {
    let grid = get_grid();
    let outside_boundary = fill(&grid);

    answer::part1(4288, compute_surface_area(&grid, |point| !grid.contains(point)));
    answer::part2(2494, compute_surface_area(&grid, |point| outside_boundary.contains(point)));
}

fn compute_surface_area(grid: &Grid<char>, f: impl Fn(&Point) -> bool) -> i64 {
    let mut surface_area = 0;
    for point in grid.points() {
        for neighbor in &point.neighbors() {
            if f(neighbor) {
                surface_area += 1;
            }
        }
    }
    surface_area
}

fn fill(grid: &Grid<char>) -> HashSet<Point> {
    let mut seen = HashSet::new();
    let bounds = grid.bounds(1);

    let mut q = Queue::new();
    q.add(bounds.lower().clone()).unwrap();
    while q.size() != 0 {
        let point = q.remove().unwrap();
        for neighbor in point.neighbors() {
            if !seen.contains(&neighbor) && !grid.contains(&neighbor) && bounds.contain(&neighbor) {
                q.add(neighbor.clone()).unwrap();
                seen.insert(neighbor.clone());
            }
        }
    }

    seen
}

fn get_grid() -> Grid<char> {
    let points = reader::read_points();
    let mut grid = Grid::new();
    points.into_iter()
        .for_each(|point| grid.add(point, '#'));
    grid
}
