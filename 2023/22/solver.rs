use aoc_lib::answer;
use aoc_lib::point::{Direction3d, Point3d};
use aoc_lib::reader::Reader;
use fxhash::{FxHashMap, FxHashSet};

#[derive(Debug)]
enum Axis {
    X,
    Y,
    Z,
}

impl Axis {
    fn new(p1: &Point3d, p2: &Point3d) -> Option<Self> {
        match (p1.x == p2.x, p1.y == p2.y, p1.z == p2.z) {
            // Consider the unit brick to be X aligned, this is arbitrary
            (true, true, true) => Some(Self::X),
            (false, true, true) => Some(Self::X),
            (true, false, true) => Some(Self::Y),
            (true, true, false) => Some(Self::Z),
            _ => None,
        }
    }

    fn get(&self, p: &Point3d) -> i64 {
        match self {
            Self::X => p.x,
            Self::Y => p.y,
            Self::Z => p.z,
        }
    }
}

#[derive(Debug)]
struct Brick {
    id: usize,
    start: Point3d,
    end: Point3d,
    held: FxHashSet<usize>,
}

impl Brick {
    fn new(id: usize, s: &str) -> Self {
        // <Point>~<Point>
        let (p1, p2) = s.split_once('~').unwrap();
        let (p1, p2) = (p1.parse().unwrap(), p2.parse().unwrap());
        let axis = Axis::new(&p1, &p2).unwrap();
        let (v1, v2) = (axis.get(&p1), axis.get(&p2));
        let (start, end) = if v1 <= v2 { (p1, p2) } else { (p2, p1) };
        Self {
            id,
            start,
            end,
            held: FxHashSet::default(),
        }
    }

    fn points(&self, direction: Option<Direction3d>) -> Vec<Point3d> {
        let mut result = Vec::default();
        for x in self.start.x..=self.end.x {
            for y in self.start.y..=self.end.y {
                for z in self.start.z..=self.end.z {
                    let mut point = Point3d::new(x, y, z);
                    if let Some(direction) = &direction {
                        point = point.add(direction);
                    }
                    result.push(point);
                }
            }
        }
        result
    }

    fn down(&mut self) {
        self.start = self.start.add(&Direction3d::Down);
        self.end = self.end.add(&Direction3d::Down);
    }

    fn at(&self, settled: &FxHashMap<Point3d, usize>, direction: Direction3d) -> FxHashSet<usize> {
        self.points(Some(direction))
            .iter()
            .flat_map(|point| settled.get(point))
            .copied()
            .collect()
    }

    fn unsupported(&self, removed: &FxHashSet<usize>) -> bool {
        self.held.iter().all(|&support| removed.contains(&support))
    }
}

#[derive(Debug)]
struct Stack {
    bricks: Vec<Brick>,
    settled: FxHashMap<Point3d, usize>,
}

impl Stack {
    fn new(bricks: Vec<Brick>) -> Self {
        Self {
            bricks,
            settled: FxHashMap::default(),
        }
    }

    fn fall(&mut self) {
        self.bricks.sort_by_key(|brick| brick.start.z);
        for brick in self.bricks.iter_mut() {
            while brick.start.z > 1 && brick.held.is_empty() {
                brick.held = brick.at(&self.settled, Direction3d::Down);
                if brick.held.is_empty() {
                    brick.down();
                }
            }
            brick.points(None).into_iter().for_each(|point| {
                self.settled.insert(point, brick.id);
            });
        }
    }

    fn counts(&mut self) -> Vec<usize> {
        self.bricks.sort_by_key(|brick| brick.id);
        self.bricks
            .iter()
            .map(|brick| {
                let mut removed = FxHashSet::default();
                self.count(&mut removed, brick)
            })
            .collect()
    }

    fn count(&self, removed: &mut FxHashSet<usize>, brick: &Brick) -> usize {
        removed.insert(brick.id);
        let holding: FxHashSet<usize> = brick
            .at(&self.settled, Direction3d::Up)
            .into_iter()
            .filter(|id| *id != brick.id)
            .collect();
        let would_fall: Vec<&Brick> = holding
            .into_iter()
            .filter_map(|id| self.bricks.get(id))
            .filter(|brick| brick.unsupported(removed))
            .collect();
        let reaction: usize = would_fall
            .iter()
            .map(|brick| self.count(removed, brick))
            .sum();
        would_fall.len() + reaction
    }
}

fn main() {
    answer::timer(solution);
}

fn solution() {
    let bricks: Vec<Brick> = Reader::default()
        .read_lines()
        .iter()
        .enumerate()
        .map(|(id, s)| Brick::new(id, s))
        .collect();

    let mut stack = Stack::new(bricks);
    stack.fall();
    let counts = stack.counts();
    answer::part1(519, counts.iter().filter(|count| **count == 0).count());
    answer::part2(109531, counts.iter().sum());
}
