use aoc_lib::answer;
use aoc_lib::collections::HashSet;
use aoc_lib::grid::{Bounds, Grid};
use aoc_lib::point::{Direction, Point};
use aoc_lib::reader::Reader;
use std::collections::VecDeque;

#[derive(Debug, Clone, PartialEq, Eq, Hash)]
struct Blizzard {
    position: Point,
    direction: Direction,
}

impl Blizzard {
    fn next(&self, valley: &Valley) -> Self {
        let suggested_position = self.position.add(&self.direction);
        let next_position = if valley.valid_position(&suggested_position) {
            suggested_position
        } else {
            let (x, y) = (self.position.x, self.position.y);
            match self.direction {
                Direction::Up => Point::new(x, valley.end().y - 1),
                Direction::Right => Point::new(valley.start().x, y),
                Direction::Down => Point::new(x, valley.start().y + 1),
                Direction::Left => Point::new(valley.end().x, y),
            }
        };
        Self {
            position: next_position,
            direction: self.direction.clone(),
        }
    }
}

#[derive(Debug, Clone)]
struct Valley {
    bounds: Bounds,
    blizzards: HashSet<Blizzard>,
    blizzard_positions: HashSet<Point>,
}

impl Valley {
    fn new(grid: Grid<char>) -> Self {
        let mut blizzards = HashSet::default();
        let mut blizzard_positions = HashSet::default();
        grid.iter()
            .filter(|(_, value)| **value != '.')
            .for_each(|(point, value)| {
                blizzard_positions.insert(point.clone());
                blizzards.insert(Blizzard {
                    position: point.clone(),
                    direction: value.to_string().parse().unwrap(),
                });
            });
        Self {
            bounds: grid.bounds(),
            blizzards,
            blizzard_positions,
        }
    }

    fn start(&self) -> &Point {
        &self.bounds.lower
    }

    fn end(&self) -> &Point {
        &self.bounds.upper
    }

    fn search(&mut self, start: &Point, end: &Point) -> Option<i64> {
        let mut q: VecDeque<Point> = VecDeque::default();
        q.push_back(start.clone());

        let mut minutes = 0;
        while !q.is_empty() {
            let mut next_states: HashSet<Point> = HashSet::default();
            while !q.is_empty() {
                let current = q.pop_front().unwrap();
                if &current == end {
                    return Some(minutes);
                }

                next_states.insert(current.clone());
                current
                    .neighbors()
                    .into_iter()
                    .filter(|next_pos| self.valid_position(next_pos))
                    .for_each(|next_pos| {
                        next_states.insert(next_pos);
                    });
            }

            self.next();
            next_states
                .into_iter()
                .filter(|next_state| !self.hits_blizzard(next_state))
                .for_each(|next_state| {
                    q.push_back(next_state);
                });
            minutes += 1;
        }
        None
    }

    fn next(&mut self) {
        let mut next_blizzards = HashSet::default();
        let mut next_blizzard_positions = HashSet::default();

        self.blizzards.iter().for_each(|blizzard| {
            let next_blizzard = blizzard.next(self);
            next_blizzard_positions.insert(next_blizzard.position.clone());
            next_blizzards.insert(next_blizzard);
        });

        self.blizzards = next_blizzards;
        self.blizzard_positions = next_blizzard_positions;
    }

    fn valid_position(&self, position: &Point) -> bool {
        if !self.bounds.contain(position) {
            return false;
        }
        // Only the start and end are valid at the ends of the y-axis
        if position.y == self.start().y || position.y == self.end().y {
            return position == self.start() || position == self.end();
        }
        true
    }

    fn hits_blizzard(&self, state: &Point) -> bool {
        self.blizzard_positions.contains(state)
    }
}

fn main() {
    answer::timer(solution);
}

fn solution() {
    let mut valley = Valley::new(Reader::default().read_grid(|ch| match ch {
        '<' | '^' | '>' | 'v' | '.' => Some(ch),
        _ => None,
    }));
    let (start, end) = (valley.start().clone(), valley.end().clone());
    let to_end = valley.search(&start, &end).unwrap();
    let to_start = valley.search(&end, &start).unwrap();
    let and_back = valley.search(&start, &end).unwrap();
    answer::part1(277, to_end);
    answer::part2(877, to_end + to_start + and_back);
}
