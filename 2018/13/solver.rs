use aoc::{answer, Direction, FromChar, Grid, HashMap, Point, Reader};

#[derive(Debug)]
enum Motion {
    Intersection,
    Forward(Direction, Direction),
}

#[derive(Debug)]
enum Tile {
    Intersection,
    Vertical,
    Horizontal,
    ForwardSlash,
    BackSlash,
}

impl FromChar for Tile {
    fn from_char(ch: char) -> Option<Self> {
        match ch {
            '+' => Some(Self::Intersection),
            '|' | '^' | 'v' => Some(Self::Vertical),
            '-' | '<' | '>' => Some(Self::Horizontal),
            '/' => Some(Self::ForwardSlash),
            '\\' => Some(Self::BackSlash),
            _ => None,
        }
    }
}

impl Tile {
    fn bottom(&self) -> bool {
        matches!(self, Self::Intersection | Self::Vertical)
    }

    fn motion(&self, bottom: bool) -> Motion {
        match self {
            Self::Intersection => Motion::Intersection,
            Self::Vertical => Motion::Forward(Direction::Up, Direction::Down),
            Self::Horizontal => Motion::Forward(Direction::Left, Direction::Right),
            Self::ForwardSlash => {
                if bottom {
                    Motion::Forward(Direction::Up, Direction::Left)
                } else {
                    Motion::Forward(Direction::Down, Direction::Right)
                }
            }
            Self::BackSlash => {
                if bottom {
                    Motion::Forward(Direction::Up, Direction::Right)
                } else {
                    Motion::Forward(Direction::Down, Direction::Left)
                }
            }
        }
    }
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
    track: Grid<Tile>,
    carts: Vec<Cart>,
    crashes: Vec<Point>,
}

impl CartSystem {
    fn new(lines: &Vec<String>) -> Self {
        let track: Grid<Tile> = lines.into();
        let carts: Grid<Direction> = lines.into();
        let carts = carts
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

        let mut carts: HashMap<Point, usize> = self
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
            let bottom = match self.track.get(&above) {
                None => false,
                Some(tile) => tile.bottom(),
            };
            let motion = self.track[&start].motion(bottom);
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
