use aoc_lib::answer;
use aoc_lib::grid::Grid;
use aoc_lib::point::Point;
use aoc_lib::reader;
use priority_queue::PriorityQueue;
use std::collections::HashSet;

fn main() {
    let (grid, start, end) = get_graph();
    answer::part1(472, bfs(&grid, &start, &end).unwrap());
    answer::part2(465, shortest_bfs(&grid, &end));
}

fn shortest_bfs(grid: &Grid<i64>, end: &Point) -> i64 {
    grid.points_with_value(get_offset('a')).iter()
        .map(|start| bfs(grid, start, end))
        .filter(|result| result.is_some())
        .map(|result| result.unwrap())
        .min()
        .unwrap()
}

fn bfs(grid: &Grid<i64>, start: &Point, end: &Point) -> Option<i64> {
    let mut queue = PriorityQueue::new();
    queue.push(start.clone(), 0);

    let mut seen: HashSet<Point> = HashSet::new();
    
    while !queue.is_empty() {
        let (point, distance) = queue.pop().unwrap();
        if point == end.clone() {
            return Some(distance * -1);
        } else {
            seen.insert(point.clone());
        }

        let max_height = grid.get(&point) + 1;
        for neighbor in point.neighbors() {
            if !seen.contains(&neighbor) && can_go(grid, &neighbor, &max_height) {
                queue.push_increase(neighbor, distance - 1);
            }
        }
    }

    return None
}

fn can_go(grid: &Grid<i64>, point: &Point, max_height: &i64) -> bool {
    grid.contains(point) && grid.get(point) <= max_height
}

fn get_graph() -> (Grid<i64>, Point, Point) {
    let mut grid = reader::read_grid(|ch| get_offset(ch));
    let mut start = Point::new_2d(0, 0);
    let mut end = Point::new_2d(0, 0);

    for p in grid.points() {
        let value = grid.get(p);
        if value == &get_offset('S') {
            start = p.to_owned().clone();
        }
        if value == &get_offset('E') {
            end = p.to_owned().clone();
        }
    }

    grid.add(start.clone(), get_offset('a'));
    grid.add(end.clone(), get_offset('z'));

    (grid, start, end)
}

fn get_offset(ch: char) -> i64 {
    (ch as i64) - ('a' as i64)
}
