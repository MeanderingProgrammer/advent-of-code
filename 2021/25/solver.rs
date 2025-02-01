use aoc::{answer, Grid, HashSet, Point, Reader};

#[derive(Debug)]
enum Cucumber {
    East,
    South,
}

impl From<&Cucumber> for Point {
    fn from(value: &Cucumber) -> Self {
        match value {
            Cucumber::South => Self::new(0, 1),
            Cucumber::East => Self::new(1, 0),
        }
    }
}

impl Cucumber {
    fn from_char(ch: char) -> Option<Cucumber> {
        match ch {
            '>' => Some(Self::East),
            'v' => Some(Self::South),
            _ => None,
        }
    }
}

#[derive(Debug)]
struct Seafloor {
    limit: Point,
    east: HashSet<Point>,
    south: HashSet<Point>,
}

impl Seafloor {
    fn new(grid: Grid<Cucumber>) -> Self {
        let mut east = HashSet::default();
        let mut south = HashSet::default();
        for (point, value) in grid.iter() {
            match value {
                Cucumber::East => {
                    east.insert(point.clone());
                }
                Cucumber::South => {
                    south.insert(point.clone());
                }
            }
        }
        Self {
            limit: grid.bounds().upper,
            east,
            south,
        }
    }

    fn converge(&mut self) -> usize {
        let mut result = 0;
        while self.step() {
            result += 1;
        }
        result + 1
    }

    fn step(&mut self) -> bool {
        let (east, east_moved) = self.apply(Cucumber::East);
        self.east = east;
        let (south, south_moved) = self.apply(Cucumber::South);
        self.south = south;
        east_moved || south_moved
    }

    fn apply(&self, cucumber: Cucumber) -> (HashSet<Point>, bool) {
        let (current, other) = match cucumber {
            Cucumber::East => (&self.east, &self.south),
            Cucumber::South => (&self.south, &self.east),
        };
        let (mut next, mut moved) = (HashSet::default(), false);
        for start in current {
            let mut point = start.add(&cucumber);
            point.x %= self.limit.x + 1;
            point.y %= self.limit.y + 1;
            if !current.contains(&point) && !other.contains(&point) {
                next.insert(point);
                moved = true;
            } else {
                next.insert(start.clone());
            }
        }
        (next, moved)
    }
}

fn main() {
    answer::timer(solution);
}

fn solution() {
    let grid = Reader::default().read_grid(Cucumber::from_char);
    let mut seafloor = Seafloor::new(grid);
    answer::part1(492, seafloor.converge());
}
