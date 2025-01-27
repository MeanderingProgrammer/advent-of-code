use aoc_lib::answer;
use aoc_lib::grid::Grid;
use aoc_lib::point::Point;
use aoc_lib::reader::Reader;
use aoc_lib::search::GraphSearch;

#[derive(Debug)]
struct Search {
    grid: Grid<i64>,
    end: Point,
}

impl GraphSearch for Search {
    type T = Point;

    fn first(&self) -> bool {
        true
    }

    fn done(&self, node: &Self::T) -> bool {
        node == &self.end
    }

    fn neighbors(&self, node: &Self::T) -> impl Iterator<Item = Self::T> {
        let max = self.grid[node] + 1;
        node.neighbors()
            .into_iter()
            .filter(move |neighbor| self.grid.has(neighbor) && self.grid[neighbor] <= max)
    }
}

impl Search {
    fn shortest(&self, start_value: i64) -> Option<i64> {
        self.grid
            .values(start_value)
            .into_iter()
            .filter_map(|start| self.bfs(start).first().cloned())
            .min()
    }
}

fn main() {
    answer::timer(solution);
}

fn solution() {
    let (search, start) = get_search();
    answer::part1(472, search.bfs(start).first().cloned().unwrap());
    answer::part2(465, search.shortest(get_offset('a')).unwrap());
}

fn get_search() -> (Search, Point) {
    let mut grid = Reader::default().read_grid(|ch| Some(get_offset(ch)));

    let start = grid.value(get_offset('S'));
    grid.add(start.clone(), get_offset('a'));

    let end = grid.value(get_offset('E'));
    grid.add(end.clone(), get_offset('z'));

    (Search { grid, end }, start)
}

fn get_offset(ch: char) -> i64 {
    (ch as i64) - ('a' as i64)
}
