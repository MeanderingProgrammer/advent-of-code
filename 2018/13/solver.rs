use aoc_lib::answer;
use aoc_lib::grid::Grid;
use aoc_lib::point::{Direction, Point};
use aoc_lib::reader::Reader;
use fxhash::FxHashMap;

#[derive(Debug)]
enum Motion {
    Intersection,
    Forward(Direction, Direction),
}

#[derive(Debug)]
struct Cart {
    id: usize,
    point: Point,
    direction: Direction,
    choices: usize,
}

impl Cart {
    fn new(id: usize, point: &Point, direction: &Direction) -> Self {
        Self {
            id,
            point: point.clone(),
            direction: direction.clone(),
            choices: 0,
        }
    }

    fn go(&mut self, motion: Motion) {
        let (direction, choice) = match motion {
            Motion::Intersection => (self.intersection(), true),
            Motion::Forward(d1, d2) => (self.forward(d1, d2), false),
        };
        self.point = self.point.add(&direction);
        self.direction = direction;
        self.choices += if choice { 1 } else { 0 };
    }

    fn intersection(&self) -> Direction {
        match self.choices % 3 {
            0 => self.direction.left(),
            1 => self.direction.clone(),
            2 => self.direction.right(),
            _ => unreachable!(),
        }
    }

    fn forward(&self, d1: Direction, d2: Direction) -> Direction {
        let opposite = self.direction.opposite();
        match (d1 == opposite, d2 == opposite) {
            (true, false) => d2,
            (false, true) => d1,
            _ => unreachable!(),
        }
    }
}

#[derive(Debug)]
struct CartSystem {
    track: Grid<char>,
    carts: Vec<Cart>,
    crashes: Vec<Point>,
}

impl CartSystem {
    fn new(lines: &[String]) -> Self {
        let track = Grid::from_lines(lines, |_, ch| match ch {
            ' ' => None,
            '<' | '>' => Some('-'),
            '^' | 'v' => Some('|'),
            ch => Some(ch),
        });
        let carts = Grid::from_lines(lines, |_, ch| Direction::from_char(ch))
            .iter()
            .enumerate()
            .map(|(id, (point, direction))| Cart::new(id, point, direction))
            .collect();
        Self {
            track,
            carts,
            crashes: Vec::default(),
        }
    }

    fn run(&mut self) {
        while self.carts.len() > 1 {
            self.tick();
        }
    }

    fn tick(&mut self) {
        self.carts.sort_by_key(|cart| cart.point.clone());

        let mut carts: FxHashMap<Point, usize> = self
            .carts
            .iter()
            .map(|cart| (cart.point.clone(), cart.id))
            .collect();

        let mut crashed = Vec::default();
        for cart in self.carts.iter_mut() {
            if crashed.contains(&cart.id) {
                continue;
            }

            let start = cart.point.clone();
            carts.remove(&start);

            let above = start.add(&Direction::Up);
            let motion = Self::motion(self.track[&start], self.track.get_or(&above, ' '));
            cart.go(motion);

            let end = cart.point.clone();
            let id = carts.remove(&end);

            match id {
                None => {
                    carts.insert(end, cart.id);
                }
                Some(id) => {
                    self.crashes.push(end);
                    crashed.append(&mut vec![id, cart.id]);
                }
            }
        }
        self.carts.retain(|cart| !crashed.contains(&cart.id));
    }

    fn motion(value: char, above: char) -> Motion {
        let bottom = ['|', '+'].contains(&above);
        match value {
            '+' => Motion::Intersection,
            '|' => Motion::Forward(Direction::Up, Direction::Down),
            '-' => Motion::Forward(Direction::Left, Direction::Right),
            '/' => {
                if bottom {
                    Motion::Forward(Direction::Up, Direction::Left)
                } else {
                    Motion::Forward(Direction::Down, Direction::Right)
                }
            }
            '\\' => {
                if bottom {
                    Motion::Forward(Direction::Up, Direction::Right)
                } else {
                    Motion::Forward(Direction::Down, Direction::Left)
                }
            }
            _ => unreachable!(),
        }
    }
}

fn main() {
    answer::timer(solution);
}

fn solution() {
    let lines = Reader::default().read_lines();
    let mut system = CartSystem::new(&lines);
    system.run();
    answer::part1("(86, 118)", &system.crashes[0].to_string());
    answer::part2("(2, 81)", &system.carts[0].point.to_string());
}
