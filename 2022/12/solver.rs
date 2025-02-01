use aoc::{answer, Base, GraphSearch, Grid, Point, Reader};

#[derive(Debug)]
struct Search {
    grid: Grid<u8>,
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
    fn shortest(&self, value: u8) -> Option<i64> {
        self.grid
            .values(&value)
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
    answer::part2(465, search.shortest(Base::ch_lower('a')).unwrap());
}

fn get_search() -> (Search, Point) {
    let mut grid = Reader::default().read_grid(|ch| Some(Base::ch_lower(ch)));

    let start = grid.value(&Base::ch_lower('S'));
    grid.add(start.clone(), Base::ch_lower('a'));

    let end = grid.value(&Base::ch_lower('E'));
    grid.add(end.clone(), Base::ch_lower('z'));

    (Search { grid, end }, start)
}
