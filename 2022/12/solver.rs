use aoc_lib::answer;
use aoc_lib::grid::Grid;
use aoc_lib::point::Point;
use aoc_lib::reader;
use aoc_lib::search::Search;

fn main() {
    answer::timer(solution);
}

fn solution() {
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
    Search {
        start: start.clone(),
        is_done: |node| node == end,
        get_neighbors: |node| {
            let max_height = grid.get(node) + 1;
            node.neighbors()
                .into_iter()
                .filter(|neighbor| grid.contains(neighbor) && grid.get(neighbor) <= &max_height)
                .map(|neighbor| (neighbor, 1))
                .collect()
        },
    }
    .dijkstra()
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
