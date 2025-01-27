use aoc_lib::answer;
use aoc_lib::grid::Grid;
use aoc_lib::point::Point;
use aoc_lib::reader::Reader;
use aoc_lib::search::Dijkstra;

#[derive(Debug)]
struct Graph {
    grid: Grid<u8>,
    tile: i64,
    total: i64,
}

impl Graph {
    fn new(grid: &Grid<u8>, expand: i64) -> Self {
        let bounds = grid.bounds();
        assert_eq!(Point::default(), bounds.lower);
        let end = bounds.upper;
        assert_eq!(end.x, end.y);
        let tile = end.x + 1;
        Self {
            grid: grid.clone(),
            tile,
            total: tile * expand,
        }
    }

    fn risk(&self, p: &Point) -> Option<u8> {
        if p.x < 0 || p.y < 0 || p.x >= self.total || p.y >= self.total {
            return None;
        }
        let base = Point::new(p.x % self.tile, p.y % self.tile);
        let original = self.grid[&base];
        let distance = ((p.x / self.tile) + (p.y / self.tile)) as u8;
        let result = original + distance;
        Some(if result > 9 { result - 9 } else { result })
    }
}

impl Dijkstra for Graph {
    type T = Point;
    type W = i64;

    fn done(&self, node: &Self::T) -> bool {
        node == &Point::new(self.total - 1, self.total - 1)
    }

    fn neighbors(&self, node: &Self::T) -> impl Iterator<Item = (Self::T, Self::W)> {
        node.neighbors()
            .into_iter()
            .filter_map(|point| self.risk(&point).map(|risk| (point, risk as i64)))
    }
}

fn main() {
    answer::timer(solution);
}

fn solution() {
    let grid = Reader::default().read_grid(|ch| Some(ch as u8 - b'0'));
    answer::part1(656, solve(&grid, 1));
    answer::part2(2979, solve(&grid, 5));
}

fn solve(grid: &Grid<u8>, expand: i64) -> i64 {
    let graph = Graph::new(grid, expand);
    graph.run(Point::default()).unwrap()
}
