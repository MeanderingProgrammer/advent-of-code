use aoc_lib::answer;
use aoc_lib::grid::Grid;
use aoc_lib::point::Point;
use aoc_lib::reader;
use itertools::Itertools;
use std::collections::{HashMap, HashSet};

type Loc = (i64, i64);
type Dir = (Loc, Loc, Loc);

const N: Loc = (0, 1);
const NE: Loc = (1, 1);
const E: Loc = (1, 0);
const SE: Loc = (1, -1);
const S: Loc = (0, -1);
const SW: Loc = (-1, -1);
const W: Loc = (-1, 0);
const NW: Loc = (-1, 1);

const NEIGHBORS: [Loc; 8] = [N, NE, E, SE, S, SW, W, NW];

const NORTH: Dir = (NW, N, NE);
const SOUTH: Dir = (SW, S, SE);
const WEST: Dir = (NW, W, SW);
const EAST: Dir = (NE, E, SE);

const CHECK_ORDER: [Dir; 4] = [NORTH, SOUTH, WEST, EAST];

#[derive(Debug, Clone)]
struct Elves {
    locations: HashSet<Loc>,
    round: usize,
}

impl Elves {
    fn apply(&mut self) -> bool {
        let proposed_locations = self.get_proposed_locations();
        let end_to_proposals = proposed_locations.values().counts();

        let mut any_move = false;
        self.locations = proposed_locations
            .iter()
            .map(|(&start, &end)| {
                let num_proposals = *end_to_proposals.get(&end).unwrap();
                let actual_end = if num_proposals == 1 { end } else { start };
                if start != actual_end {
                    any_move = true;
                }
                actual_end
            })
            .collect();
        self.round += 1;

        any_move
    }

    fn get_proposed_locations(&self) -> HashMap<Loc, Loc> {
        let proposals = self.get_proposals();

        let mut proposed_locations = HashMap::new();
        for (x, y) in self.locations.iter() {
            let isolated = NEIGHBORS
                .iter()
                .map(|(dx, dy)| (x + dx, y + dy))
                .all(|location| !self.locations.contains(&location));
            let new_location = if isolated {
                (*x, *y)
            } else {
                proposals
                    .iter()
                    .map(|(n1, n2, n3)| {
                        (
                            (x + n1.0, y + n1.1),
                            (x + n2.0, y + n2.1),
                            (x + n3.0, y + n3.1),
                        )
                    })
                    .filter(|(l1, l2, l3)| {
                        !self.locations.contains(&l1)
                            && !self.locations.contains(&l2)
                            && !self.locations.contains(&l3)
                    })
                    .map(|(_, l2, _)| l2)
                    .next()
                    .unwrap_or((*x, *y))
            };
            proposed_locations.insert((*x, *y), new_location);
        }
        proposed_locations
    }

    fn get_proposals(&self) -> Vec<Dir> {
        CHECK_ORDER
            .iter()
            .cycle()
            .skip(self.round % 4)
            .take(4)
            .map(|&proposal| proposal)
            .collect()
    }

    fn empty_tiles(&self) -> i64 {
        let grid = self.as_grid();
        let total_size = grid.bounds(0).size();
        let occupied = i64::try_from(grid.points().len()).unwrap();
        total_size - occupied
    }

    fn as_grid(&self) -> Grid<char> {
        let mut grid = Grid::new();
        self.locations
            .iter()
            .map(|(x, y)| Point::new_2d(*x, -*y))
            .for_each(|point| grid.add(point, '#'));
        grid
    }
}

fn main() {
    let (empty_tiles, total_rounds) = simulate_until_end();
    answer::part1(4070, empty_tiles);
    answer::part2(881, total_rounds);
}

fn simulate_until_end() -> (i64, usize) {
    let mut elves = get_elves();
    let mut round_10 = None;

    let mut any_move = true;
    while any_move {
        any_move = elves.apply();
        if elves.round == 10 {
            round_10 = Some(elves.empty_tiles());
        }
    }
    (round_10.unwrap(), elves.round)
}

fn get_elves() -> Elves {
    let grid = reader::read_grid(|ch| Some(ch));
    Elves {
        locations: grid
            .points_with_value('#')
            .iter()
            .map(|elve| (elve.x(), -elve.y()))
            .collect(),
        round: 0,
    }
}
