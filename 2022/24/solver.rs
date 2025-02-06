use aoc::{answer, Direction, FromChar, Grid, HashSet, Point, Reader};
use std::collections::VecDeque;

#[derive(Debug, Clone, PartialEq, Eq, Hash)]
struct Blizzard {
    position: Point,
    direction: Direction,
}

impl Blizzard {
    fn next(&self, valley: &Valley) -> Self {
        let suggested_position = self.position.add(&self.direction);
        let next_position = if valley.contains(&suggested_position) {
            suggested_position
        } else {
            let (x, y) = (self.position.x, self.position.y);
            match self.direction {
                Direction::Up => Point::new(x, valley.end.y - 1),
                Direction::Right => Point::new(valley.start.x, y),
                Direction::Down => Point::new(x, valley.start.y + 1),
                Direction::Left => Point::new(valley.end.x, y),
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
    start: Point,
    end: Point,
    positions: HashSet<Point>,
    blizzards: HashSet<Blizzard>,
}

impl Valley {
    fn new(grid: Grid<char>) -> Self {
        let bounds = grid.bounds();
        let mut positions = HashSet::default();
        let mut blizzards = HashSet::default();
        for (point, value) in grid.iter() {
            if let Some(direction) = Direction::from_char(*value) {
                positions.insert(point.clone());
                blizzards.insert(Blizzard {
                    position: point.clone(),
                    direction,
                });
            }
        }
        Self {
            start: bounds.lower.add(&Direction::Right),
            end: bounds.upper.add(&Direction::Left),
            positions,
            blizzards,
        }
    }

    fn search(&mut self, start: &Point, end: &Point) -> Option<i64> {
        let mut q: VecDeque<Point> = VecDeque::default();
        q.push_back(start.clone());

        let mut minutes = 0;
        while !q.is_empty() {
            let mut next_states: HashSet<Point> = HashSet::default();
            while let Some(current) = q.pop_front() {
                if &current == end {
                    return Some(minutes);
                }

                next_states.insert(current.clone());
                current
                    .neighbors()
                    .into_iter()
                    .filter(|next_pos| self.contains(next_pos))
                    .for_each(|next_pos| {
                        next_states.insert(next_pos);
                    });
            }

            self.next();
            next_states
                .into_iter()
                .filter(|next_state| !self.positions.contains(next_state))
                .for_each(|next_state| q.push_back(next_state));
            minutes += 1;
        }
        None
    }

    fn next(&mut self) {
        let mut next_positions = HashSet::default();
        let mut next_blizzards = HashSet::default();
        self.blizzards.iter().for_each(|blizzard| {
            let next_blizzard = blizzard.next(self);
            next_positions.insert(next_blizzard.position.clone());
            next_blizzards.insert(next_blizzard);
        });
        self.positions = next_positions;
        self.blizzards = next_blizzards;
    }

    fn contains(&self, Point { x, y }: &Point) -> bool {
        if *x < self.start.x || *x > self.end.x {
            return false;
        }
        if *y < self.start.y || *y > self.end.y {
            return false;
        }
        // Only the start and end are valid at the ends of the y-axis
        if *y == self.start.y && *x != self.start.x {
            return false;
        }
        if *y == self.end.y && *x != self.end.x {
            return false;
        }
        true
    }
}

fn main() {
    answer::timer(solution);
}

fn solution() {
    let mut valley = Valley::new(Reader::default().grid());
    let (start, end) = (valley.start.clone(), valley.end.clone());
    let to_end = valley.search(&start, &end).unwrap();
    let to_start = valley.search(&end, &start).unwrap();
    let and_back = valley.search(&start, &end).unwrap();
    answer::part1(277, to_end);
    answer::part2(877, to_end + to_start + and_back);
}
