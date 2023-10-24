use aoc_lib::answer;
use aoc_lib::grid::Grid;
use aoc_lib::point::Point;
use aoc_lib::reader;
use priority_queue::PriorityQueue;
use std::collections::HashSet;

fn main() {
    let (grid, start, end) = get_graph();
    answer::part1(472, bfs(&grid, &start, &end).unwrap());
    answer::part2(465, shortest_bfs(&grid, &end).unwrap());
}

fn shortest_bfs(grid: &Grid<i64>, end: &Point) -> Option<i64> {
    grid.points_with_value(get_offset('a'))
        .iter()
        .map(|start| bfs(grid, start, end))
        .filter(|result| result.is_some())
        .map(|result| result.unwrap())
        .min()
}

fn bfs(grid: &Grid<i64>, start: &Point, end: &Point) -> Option<i64> {
    let mut queue = PriorityQueue::new();
    queue.push(start.clone(), 0);
    let mut seen: HashSet<Point> = HashSet::new();
    while !queue.is_empty() {
        let (point, distance) = queue.pop().unwrap();
        if &point == end {
            return Some(distance * -1);
        }
        seen.insert(point.clone());
        let max_height = grid.get(&point) + 1;
        for neighbor in point.neighbors() {
            if !seen.contains(&neighbor) && can_go(grid, &neighbor, &max_height) {
                queue.push_increase(neighbor, distance - 1);
            }
        }
    }
    None
}

fn can_go(grid: &Grid<i64>, point: &Point, max_height: &i64) -> bool {
    grid.contains(point) && grid.get(point) <= max_height
}

fn get_graph() -> (Grid<i64>, Point, Point) {
    let mut grid = reader::read_grid(|ch| Some(get_offset(ch)));

    let start = grid.points_with_value(get_offset('S'))[0].clone();
    grid.add(start.clone(), get_offset('a'));

    let end = grid.points_with_value(get_offset('E'))[0].clone();
    grid.add(end.clone(), get_offset('z'));

    (grid, start.clone(), end.clone())
}

fn get_offset(ch: char) -> i64 {
    (ch as i64) - ('a' as i64)
}
