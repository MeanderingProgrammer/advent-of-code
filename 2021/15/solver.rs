use aoc::{answer, Dijkstra, Grid, Point, Reader};

#[derive(Debug)]
struct Graph {
    grid: Grid<u8>,
    tile: i32,
    total: i32,
}

impl Graph {
    fn new(grid: &Grid<u8>, expand: i32) -> Self {
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
    type W = u16;

    fn done(&self, node: &Self::T) -> bool {
        node == &Point::new(self.total - 1, self.total - 1)
    }

    fn neighbors(&self, node: &Self::T) -> impl Iterator<Item = (Self::T, Self::W)> {
        node.neighbors()
            .into_iter()
            .filter_map(|point| self.risk(&point).map(|risk| (point, risk as u16)))
    }
}

fn main() {
    answer::timer(solution);
}

fn solution() {
    let grid = Reader::default().grid();
    answer::part1(656, solve(&grid, 1));
    answer::part2(2979, solve(&grid, 5));
}

fn solve(grid: &Grid<u8>, expand: i32) -> u16 {
    let graph = Graph::new(grid, expand);
    graph.run(Point::default()).unwrap()
}
