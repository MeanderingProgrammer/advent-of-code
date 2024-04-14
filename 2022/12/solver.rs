use aoc_lib::answer;
use aoc_lib::grid::Grid;
use aoc_lib::point::Point;
use aoc_lib::reader::Reader;
use aoc_lib::search::GraphTraversal;

#[derive(Debug)]
struct Search {
    grid: Grid<i64>,
    end: Point,
}

impl GraphTraversal for Search {
    type T = Point;

    fn done(&self, node: &Point) -> bool {
        node == &self.end
    }

    fn neighbors(&self, node: &Point) -> impl Iterator<Item = Point> {
        let max_height = self.grid.get(node) + 1;
        node.neighbors().into_iter().filter(move |neighbor| {
            self.grid.contains(neighbor) && self.grid.get(neighbor) <= &max_height
        })
    }
}

impl Search {
    fn shortest(&self, start_value: i64) -> Option<i64> {
        self.grid
            .points_with_value(start_value)
            .iter()
            .filter_map(|start| self.bfs(start))
            .min()
    }
}

fn main() {
    answer::timer(solution);
}

fn solution() {
    let (search, start) = get_search();
    answer::part1(472, search.bfs(&start).unwrap());
    answer::part2(465, search.shortest(get_offset('a')).unwrap());
}

fn get_search() -> (Search, Point) {
    let mut grid = Reader::default().read_grid(|ch| Some(get_offset(ch)));

    let start = grid.points_with_value(get_offset('S'))[0].clone();
    grid.add(start.clone(), get_offset('a'));

    let end = grid.points_with_value(get_offset('E'))[0].clone();
    grid.add(end.clone(), get_offset('z'));

    (Search { grid, end }, start)
}

fn get_offset(ch: char) -> i64 {
    (ch as i64) - ('a' as i64)
}
