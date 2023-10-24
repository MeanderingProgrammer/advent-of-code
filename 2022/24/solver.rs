use aoc_lib::answer;
use aoc_lib::grid::{Bound, Grid};
use aoc_lib::point::Point;
use aoc_lib::reader;
use queues::{IsQueue, Queue};
use std::collections::HashSet;

#[derive(Debug, Clone, PartialEq, Eq, Hash)]
enum Direction {
    Up,
    Right,
    Down,
    Left,
}

impl Direction {
    fn from_ch(ch: &char) -> Self {
        match ch {
            '^' => Direction::Up,
            '>' => Direction::Right,
            'v' => Direction::Down,
            '<' => Direction::Left,
            _ => unreachable!(),
        }
    }

    fn next(&self, position: &Point) -> Point {
        match self {
            Self::Up => position.add_y(-1),
            Self::Right => position.add_x(1),
            Self::Down => position.add_y(1),
            Self::Left => position.add_x(-1),
        }
    }
}

#[derive(Debug, Clone, PartialEq, Eq, Hash)]
struct Blizzard {
    position: Point,
    direction: Direction,
}

impl Blizzard {
    fn next(&self, valley: &Valley) -> Self {
        let suggested_position = self.direction.next(&self.position);
        let next_position = if valley.valid_position(&suggested_position) {
            suggested_position
        } else {
            let (x, y) = (self.position.x(), self.position.y());
            match self.direction {
                Direction::Up => Point::new_2d(x, valley.end().y() - 1),
                Direction::Right => Point::new_2d(valley.start().x(), y),
                Direction::Down => Point::new_2d(x, valley.start().y() + 1),
                Direction::Left => Point::new_2d(valley.end().x(), y),
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
    bounds: Bound,
    blizzards: HashSet<Blizzard>,
    blizzard_positions: HashSet<Point>,
}

impl Valley {
    fn new(grid: Grid<char>) -> Self {
        let mut blizzards = HashSet::new();
        let mut blizzard_positions = HashSet::new();

        grid.points()
            .iter()
            .map(|point| (point, grid.get(point)))
            .filter(|(_, &value)| value != '.')
            .for_each(|(&point, value)| {
                blizzard_positions.insert(point.clone());
                blizzards.insert(Blizzard {
                    position: point.clone(),
                    direction: Direction::from_ch(value),
                });
            });

        let bounds = grid.bounds(0);
        Self {
            bounds,
            blizzards,
            blizzard_positions,
        }
    }

    fn start(&self) -> &Point {
        self.bounds.lower()
    }

    fn end(&self) -> &Point {
        self.bounds.upper()
    }

    fn search(&mut self, start: &Point, end: &Point) -> Option<i64> {
        let mut q: Queue<Point> = Queue::new();
        q.add(start.clone()).unwrap();

        let mut minutes = 0;
        while q.size() > 0 {
            let mut next_states: HashSet<Point> = HashSet::new();
            while q.size() > 0 {
                let current = q.remove().unwrap();
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
                    q.add(next_state).unwrap();
                });
            minutes += 1;
        }
        None
    }

    fn next(&mut self) {
        let mut next_blizzards = HashSet::new();
        let mut next_blizzard_positions = HashSet::new();

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
        if position.y() == self.start().y() || position.y() == self.end().y() {
            return position == self.start() || position == self.end();
        }
        true
    }

    fn hits_blizzard(&self, state: &Point) -> bool {
        self.blizzard_positions.contains(state)
    }
}

fn main() {
    let mut valley = Valley::new(reader::read_grid(|ch| match ch {
        '<' | '^' | '>' | 'v' | '.' => Some(ch),
        _ => None,
    }));
    let (start, end) = (valley.start().clone(), valley.end().clone());

    let to_end = valley.search(&start, &end).unwrap();
    answer::part1(277, to_end);

    let to_start = valley.search(&end, &start).unwrap();
    let and_back = valley.search(&start, &end).unwrap();
    answer::part2(877, to_end + to_start + and_back);
}
