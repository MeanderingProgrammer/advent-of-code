use aoc::{answer, Direction, FromChar, Grid, HashMap, Point, Reader};
use std::fmt;

#[derive(Debug, Clone, PartialEq)]
enum Value {
    Empty,
    Round,
    Cube,
}

impl FromChar for Value {
    fn from_char(ch: char) -> Option<Self> {
        match ch {
            '.' => Some(Self::Empty),
            'O' => Some(Self::Round),
            '#' => Some(Self::Cube),
            _ => None,
        }
    }
}

impl fmt::Display for Value {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        let value = match self {
            Self::Empty => ".",
            Self::Round => "O",
            Self::Cube => "#",
        };
        write!(f, "{}", value)
    }
}

#[derive(Debug, Clone)]
struct Platform {
    grid: Grid<Value>,
}

impl Platform {
    fn run_once(&mut self) -> i32 {
        self.move_rocks(&Direction::Up);
        self.total_load()
    }

    fn run_n(&mut self, n: usize) -> i32 {
        let mut seen: HashMap<String, (usize, i32)> = HashMap::default();
        let mut as_string = self.grid.to_string();
        while !seen.contains_key(&as_string) {
            seen.insert(as_string, (seen.len(), self.total_load()));
            self.move_rocks(&Direction::Up);
            self.move_rocks(&Direction::Left);
            self.move_rocks(&Direction::Down);
            self.move_rocks(&Direction::Right);
            as_string = self.grid.to_string();
        }

        let start = seen.get(&as_string).unwrap().0;
        let mut pattern: Vec<(usize, i32)> = seen
            .values()
            .map(|(index, load)| (*index, *load))
            .filter(|(index, _)| *index >= start)
            .collect();
        pattern.sort();
        let pattern: Vec<i32> = pattern.into_iter().map(|(_, load)| load).collect();

        pattern[(n - start) % pattern.len()]
    }

    fn move_rocks(&mut self, direction: &Direction) {
        let mut rocks = self.rocks();
        rocks.sort_unstable_by(|p1, p2| match direction {
            Direction::Up => p1.y.cmp(&p2.y),
            Direction::Down => p2.y.cmp(&p1.y),
            Direction::Left => p1.x.cmp(&p2.x),
            Direction::Right => p2.x.cmp(&p1.x),
        });
        rocks.into_iter().for_each(|rock| {
            let mut next = rock.clone();
            while self.grid.is(&next.add(direction), &Value::Empty) {
                next = next.add(direction);
            }
            if rock != next {
                self.grid.add(rock, Value::Empty);
                self.grid.add(next, Value::Round);
            }
        });
    }

    fn total_load(&self) -> i32 {
        let max_y = self.grid.bounds().upper.y + 1;
        self.rocks().into_iter().map(|point| max_y - point.y).sum()
    }

    fn rocks(&self) -> Vec<Point> {
        self.grid.values(&Value::Round)
    }
}

fn main() {
    answer::timer(solution);
}

fn solution() {
    let grid = Platform {
        grid: Reader::default().read_grid(),
    };
    answer::part1(109654, grid.clone().run_once());
    answer::part2(94876, grid.clone().run_n(1000000000));
}
