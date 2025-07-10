use aoc::prelude::*;

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
            .filter_map(|start| self.bfs(start).pop())
            .min()
    }
}

fn main() {
    answer::timer(solution);
}

fn solution() {
    let grid = Reader::default().grid();
    let (search, start) = get_search(grid);
    answer::part1(472, search.bfs(start).first().cloned().unwrap());
    answer::part2(465, search.shortest(index('a')).unwrap());
}

fn get_search(mut grid: Grid<u8>) -> (Search, Point) {
    let start = grid.value(&index('S'));
    grid.add(start.clone(), index('a'));

    let end = grid.value(&index('E'));
    grid.add(end.clone(), index('z'));

    (Search { grid, end }, start)
}

fn index(ch: char) -> u8 {
    u8::from_char(ch).unwrap()
}
