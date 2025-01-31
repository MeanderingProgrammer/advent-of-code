use aoc_lib::answer;
use aoc_lib::collections::HashSet;
use aoc_lib::grid::Grid;
use aoc_lib::iter::Iter;
use aoc_lib::point::{Heading, Point};
use aoc_lib::reader::Reader;

type Dir = (Heading, Heading, Heading);

const CHECK_ORDER: [Dir; 4] = [
    (Heading::NorthWest, Heading::North, Heading::NorthEast),
    (Heading::SouthWest, Heading::South, Heading::SouthEast),
    (Heading::NorthWest, Heading::West, Heading::SouthWest),
    (Heading::NorthEast, Heading::East, Heading::SouthEast),
];

#[derive(Debug, Clone)]
struct Elves {
    locations: HashSet<Point>,
    round: usize,
}

impl Elves {
    fn apply(&mut self) -> bool {
        let proposals: Vec<(Point, Option<Point>)> = self
            .locations
            .iter()
            .map(|location| (location.clone(), self.get_proposal(location)))
            .collect();

        let counts = proposals.iter().filter_map(|(_, end)| end.clone()).counts();

        self.round += 1;
        let mut done = true;
        self.locations = proposals
            .into_iter()
            .map(|(start, end)| match end {
                None => start,
                Some(end) => {
                    if counts[&end] > 1 {
                        start
                    } else {
                        done = false;
                        end
                    }
                }
            })
            .collect();
        !done
    }

    fn get_proposal(&self, location: &Point) -> Option<Point> {
        let isolated = location
            .diagonal_neighbors()
            .iter()
            .all(|location| !self.locations.contains(location));
        match isolated {
            true => None,
            false => CHECK_ORDER
                .iter()
                .cycle()
                .skip(self.round % 4)
                .take(4)
                .map(|(n1, n2, n3)| (location.add(n1), location.add(n2), location.add(n3)))
                .filter(|(l1, l2, l3)| {
                    !self.locations.contains(l1)
                        && !self.locations.contains(l2)
                        && !self.locations.contains(l3)
                })
                .map(|(_, l2, _)| l2)
                .next(),
        }
    }

    fn empty_tiles(&self) -> usize {
        let mut grid = Grid::default();
        self.locations
            .iter()
            .for_each(|point| grid.add(point.clone(), true));
        let total_size = grid.bounds().size() as usize;
        total_size - self.locations.len()
    }
}

fn main() {
    answer::timer(solution);
}

fn solution() {
    let grid = Reader::default().read_grid(Some);
    let elves = Elves {
        locations: grid.values(&'#').into_iter().collect(),
        round: 0,
    };
    let (part1, part2) = simulate(elves);
    answer::part1(4070, part1);
    answer::part2(881, part2);
}

fn simulate(mut elves: Elves) -> (usize, usize) {
    let mut round_10 = 0;
    while elves.apply() {
        if elves.round == 10 {
            round_10 = elves.empty_tiles();
        }
    }
    (round_10, elves.round)
}
