use aoc::prelude::*;

#[derive(Debug)]
struct Map {
    grid: Grid<u8>,
}

impl Map {
    fn results(&self) -> Vec<(usize, bool)> {
        self.grid
            .iter()
            .map(|(point, value)| self.scenic_score(point, value))
            .collect()
    }

    fn scenic_score(&self, point: &Point, score: &u8) -> (usize, bool) {
        let (mut dist, mut edge) = (1, false);
        for dir in Direction::values() {
            let (dir_dist, dir_edge) = self.go(score, point, dir);
            dist *= dir_dist;
            edge |= dir_edge;
        }
        (dist, edge)
    }

    fn go(&self, top: &u8, point: &Point, direction: &Direction) -> (usize, bool) {
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
    let grid = Reader::default().grid();
    let map = Map { grid };
    let results = map.results();
    answer::part1(1533, results.iter().filter(|score| score.1).count());
    answer::part2(345744, results.iter().map(|score| score.0).max().unwrap());
}
