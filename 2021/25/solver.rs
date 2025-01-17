use aoc_lib::answer;
use aoc_lib::grid::Grid;
use aoc_lib::point::Point;
use aoc_lib::reader::Reader;
use fxhash::FxHashSet;

#[derive(Debug)]
enum Cucumber {
    East,
    South,
}

impl Cucumber {
    fn from_char(ch: char) -> Option<Cucumber> {
        match ch {
            '>' => Some(Self::East),
            'v' => Some(Self::South),
            _ => None,
        }
    }

    fn to_point(&self) -> Point {
        match self {
            Self::South => Point::new(0, 1),
            Self::East => Point::new(1, 0),
        }
    }
}

#[derive(Debug)]
struct Seafloor {
    limit: Point,
    east: FxHashSet<Point>,
    south: FxHashSet<Point>,
}

impl Seafloor {
    fn new(grid: Grid<Cucumber>) -> Self {
        let mut east = FxHashSet::default();
        let mut south = FxHashSet::default();
        for point in grid.points() {
            match grid.get(point) {
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

    fn apply(&self, cucumber: Cucumber) -> (FxHashSet<Point>, bool) {
        let (current, other) = match cucumber {
            Cucumber::East => (&self.east, &self.south),
            Cucumber::South => (&self.south, &self.east),
        };
        let (mut next, mut moved) = (FxHashSet::default(), false);
        for start in current {
            let mut point = start.add(&cucumber.to_point());
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
