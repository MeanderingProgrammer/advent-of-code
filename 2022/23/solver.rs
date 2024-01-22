use aoc_lib::answer;
use aoc_lib::grid::Grid;
use aoc_lib::point::{Heading, Point};
use aoc_lib::reader::Reader;
use fxhash::FxHashSet;
use itertools::Itertools;

type Dir = (Heading, Heading, Heading);

const CHECK_ORDER: [Dir; 4] = [
    (Heading::NorthWest, Heading::North, Heading::NorthEast),
    (Heading::SouthWest, Heading::South, Heading::SouthEast),
    (Heading::NorthWest, Heading::West, Heading::SouthWest),
    (Heading::NorthEast, Heading::East, Heading::SouthEast),
];

#[derive(Debug, Clone)]
struct Elves {
    locations: FxHashSet<Point>,
    round: usize,
}

impl Elves {
    fn apply(&mut self) -> bool {
        let proposals = self.get_proposals();
        let end_to_proposals = proposals.iter().map(|(_, end)| end).counts();

        let mut any_move = false;
        self.locations = proposals
            .iter()
            .map(|(start, end)| {
                let num_proposals = end_to_proposals[&end];
                let actual_end = if num_proposals == 1 { end } else { start };
                if start != actual_end {
                    any_move = true;
                }
                actual_end.clone()
            })
            .collect();
        self.round += 1;

        any_move
    }

    fn get_proposals(&self) -> Vec<(Point, Point)> {
        self.locations
            .iter()
            .map(|location| (location.clone(), self.get_proposal(location)))
            .collect()
    }

    fn get_proposal(&self, location: &Point) -> Point {
        let isolated = location
            .diagonal_neighbors()
            .iter()
            .all(|location| !self.locations.contains(location));
        match isolated {
            true => location.clone(),
            false => CHECK_ORDER
                .iter()
                .cycle()
                .skip(self.round % 4)
                .take(4)
                .map(|(n1, n2, n3)| (location + n1, location + n2, location + n3))
                .filter(|(l1, l2, l3)| {
                    !self.locations.contains(l1)
                        && !self.locations.contains(l2)
                        && !self.locations.contains(l3)
                })
                .map(|(_, l2, _)| l2)
                .next()
                .unwrap_or(location.clone()),
        }
    }

    fn empty_tiles(&self) -> i64 {
        let mut grid = Grid::default();
        self.locations
            .iter()
            .for_each(|point| grid.add(point.clone(), '#'));
        let total_size = grid.bounds(0).size();
        let occupied = grid.points().len() as i64;
        total_size - occupied
    }
}

fn main() {
    answer::timer(solution);
}

fn solution() {
    let (empty_tiles, total_rounds) = simulate_until_end();
    answer::part1(4070, empty_tiles);
    answer::part2(881, total_rounds);
}

fn simulate_until_end() -> (i64, usize) {
    let mut round_10 = 0;
    let mut elves = get_elves();
    while elves.apply() {
        if elves.round == 10 {
            round_10 = elves.empty_tiles();
        }
    }
    (round_10, elves.round)
}

fn get_elves() -> Elves {
    let grid = Reader::default().read_grid(Some);
    Elves {
        locations: grid.points_with_value('#').into_iter().cloned().collect(),
        round: 0,
    }
}
