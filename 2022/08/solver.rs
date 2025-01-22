use aoc_lib::answer;
use aoc_lib::grid::Grid;
use aoc_lib::point::{Direction, Point};
use aoc_lib::reader::Reader;

#[derive(Debug)]
struct Map {
    grid: Grid<usize>,
}

impl Map {
    fn results(&self) -> Vec<(usize, bool)> {
        self.grid
            .iter()
            .map(|(point, value)| self.scenic_score(point, value))
            .collect()
    }

    fn scenic_score(&self, point: &Point, value: &usize) -> (usize, bool) {
        let (mut dist, mut edge) = (1, false);
        for dir in Direction::values() {
            let (dir_dist, dir_edge) = self.go(value, point, dir);
            dist *= dir_dist;
            edge |= dir_edge;
        }
        (dist, edge)
    }

    fn go(&self, top: &usize, point: &Point, direction: &Direction) -> (usize, bool) {
        let next = point.add(direction);
        match self.grid.get(&next) {
            None => (0, true),
            Some(value) => {
                if value >= top {
                    (1, false)
                } else {
                    let (dist, edge) = self.go(top, &next, direction);
                    (1 + dist, edge)
                }
            }
        }
    }
}

fn main() {
    answer::timer(solution);
}

fn solution() {
    let grid = Reader::default().read_grid(|ch| Some(ch.to_digit(10).unwrap() as usize));
    let map = Map { grid };
    let results = map.results();
    answer::part1(1533, results.iter().filter(|score| score.1).count());
    answer::part2(345744, results.iter().map(|score| score.0).max().unwrap());
}
