use aoc_lib::answer;
use aoc_lib::grid::{Bound, Grid};
use aoc_lib::point::Point;
use aoc_lib::reader;
use queues::{Queue, IsQueue};
use std::collections::HashSet;

#[derive(Debug, Clone, PartialEq, Eq, Hash)]
enum Direction {
    Up,
    Right,
    Down, 
    Left,
}

#[derive(Debug, Clone, PartialEq, Eq, Hash)]
struct Blizzard {
    position: Point,
    direction: Direction,
}

impl Blizzard {
    fn next(&self, valley: &Valley) -> Self {
        let suggested_position = match self.direction {
            Direction::Up    => self.position.add_y(-1),
            Direction::Right => self.position.add_x(1),
            Direction::Down  => self.position.add_y(1),
            Direction::Left  => self.position.add_x(-1),
        };
        let next_position = if valley.valid_position(&suggested_position) {
            suggested_position
        } else {
            let (x, y) = (self.position.x(), self.position.y());
            match self.direction {
                Direction::Up    => Point::new_2d(x, valley.end().y() - 1),
                Direction::Right => Point::new_2d(valley.start().x(), y),
                Direction::Down  => Point::new_2d(x, valley.start().y() + 1),
                Direction::Left  => Point::new_2d(valley.end().x(), y),
            }
        };
        Self {
            position: next_position,
            direction: self.direction.clone(),
        }
    }
}

type BlizzardGrid = Grid<char>;
type Blizzards = HashSet<Blizzard>;

#[derive(Debug, Clone)]
struct Valley {
    bounds: Bound,
    blizzards: Blizzards,
}

impl Valley {
    fn new(grid: BlizzardGrid) -> Self {
        let bounds = grid.bounds(0);
        let mut blizzards = Blizzards::new();
        grid.points().iter()
            .map(|point| (point, grid.get(point)))
            .filter(|(_, &value)| value != '.')
            .for_each(|(&point, value)| {
                let direction = match value {
                    '^' => Direction::Up,
                    '>' => Direction::Right,
                    'v' => Direction::Down,
                    '<' => Direction::Left,
                    _ => unreachable!(),
                };
                blizzards.insert(Blizzard {
                    position: point.clone(),
                    direction: direction,
                });
            });
        Self { bounds, blizzards }
    }

    fn start(&self) -> &Point {
        self.bounds.lower()
    }

    fn end(&self) -> &Point {
        self.bounds.upper()
    }

    fn next(&mut self) {
        let mut next_blizzards = Blizzards::new();
        self.blizzards.iter()
            .for_each(|blizzard| {
                next_blizzards.insert(blizzard.next(self));
            });
        self.blizzards = next_blizzards;
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

    fn hits_blizzard(&self, position: &Point) -> bool {
        self.blizzards.iter()
            .map(|blizzard| &blizzard.position)
            .any(|bliz_pos| bliz_pos == position)
    }
}

fn main() {
    let mut valley = Valley::new(reader::read_grid(|ch| match ch {
        '<' | '^' | '>' | 'v' | '.' => Some(ch),
        _ => None,    
    }));
    let (start, end) = (valley.start().clone(), valley.end().clone());

    let to_end = search(&mut valley, &start, &end);
    answer::part1(277, to_end);

    let to_start = search(&mut valley, &end, &start);
    let and_back = search(&mut valley, &start, &end);
    answer::part2(877, to_end + to_start + and_back);
}

fn search(valley: &mut Valley, start: &Point, end: &Point) -> i64 {
    let mut minutes = 0;

    let mut q: Queue<Point> = Queue::new();
    q.add(start.clone()).unwrap();

    while q.size() > 0 {
        let mut next_states: HashSet<Point> = HashSet::new();
        while q.size() > 0 {
            let current = q.remove().unwrap();
            if &current == end {
                return minutes;
            }

            next_states.insert(current.clone());
            current.neighbors().into_iter()
                .filter(|next_pos| valley.valid_position(next_pos))
                .for_each(|next_pos| {
                    next_states.insert(next_pos);
                });
        }

        valley.next();
        next_states.into_iter()
            .filter(|point| !valley.hits_blizzard(point))
            .for_each(|point| {
                q.add(point).unwrap();
            });
        minutes += 1;
    }

    panic!("Could not find solution");
}
