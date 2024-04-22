use aoc_lib::answer;
use aoc_lib::grid::Grid;
use aoc_lib::point::{Direction, Point};
use aoc_lib::reader::Reader;

#[derive(Debug, Clone, PartialEq)]
enum Value {
    Empty,
    Round,
    Cube,
}

impl Value {
    fn from_ch(ch: char) -> Option<Self> {
        match ch {
            '.' => Some(Self::Empty),
            'O' => Some(Self::Round),
            '#' => Some(Self::Cube),
            _ => None,
        }
    }
}

impl ToString for Value {
    fn to_string(&self) -> String {
        match self {
            Self::Empty => ".".to_string(),
            Self::Round => "O".to_string(),
            Self::Cube => "#".to_string(),
        }
    }
}

#[derive(Debug, Clone)]
struct Platform {
    grid: Grid<Value>,
}

impl Platform {
    fn run_once(&mut self) -> i64 {
        self.move_rocks(&Direction::Up);
        self.total_load()
    }

    fn run_n(&mut self, n: usize) -> i64 {
        let mut seen: Vec<(String, i64)> = Vec::new();
        let mut as_string = self.grid.to_string();
        while !seen.iter().any(|(value, _)| value == &as_string) {
            seen.push((as_string, self.total_load()));
            self.move_rocks(&Direction::Up);
            self.move_rocks(&Direction::Left);
            self.move_rocks(&Direction::Down);
            self.move_rocks(&Direction::Right);
            as_string = self.grid.to_string();
        }

        let preamble = seen
            .iter()
            .position(|(value, _)| value == &as_string)
            .unwrap();
        let pattern: Vec<i64> = seen
            .into_iter()
            .skip(preamble)
            .map(|(_, load)| load)
            .collect();

        pattern[(n - preamble) % pattern.len()]
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
            while self.grid.get_or(&(&next + direction)) == Some(&Value::Empty) {
                next = &next + direction;
            }
            if rock != next {
                self.grid.add(rock, Value::Empty);
                self.grid.add(next, Value::Round);
            }
        });
    }

    fn total_load(&self) -> i64 {
        let max_y = self.grid.bounds().upper.y + 1;
        self.rocks().into_iter().map(|point| max_y - point.y).sum()
    }

    fn rocks(&self) -> Vec<Point> {
        self.grid
            .points_with_value(Value::Round)
            .into_iter()
            .cloned()
            .collect()
    }
}

fn main() {
    answer::timer(solution);
}

fn solution() {
    let grid = Platform {
        grid: Reader::default().read_grid(Value::from_ch),
    };
    answer::part1(109654, grid.clone().run_once());
    answer::part1(94876, grid.clone().run_n(1000000000));
}
