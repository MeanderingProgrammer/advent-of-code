use aoc_lib::answer;
use aoc_lib::reader::Reader;
use fxhash::FxHashMap;
use std::str::FromStr;

#[derive(Debug, Clone, PartialEq, Eq, Hash)]
struct Point {
    w: i64,
    x: i64,
    y: i64,
    z: i64,
}

impl FromStr for Point {
    type Err = String;

    fn from_str(s: &str) -> Result<Self, Self::Err> {
        let values: Vec<i64> = s
            .split(',')
            .map(|coord| coord.trim().parse().unwrap())
            .collect();
        if values.len() == 4 {
            Ok(Self {
                w: values[0],
                x: values[1],
                y: values[2],
                z: values[3],
            })
        } else {
            Err(format!("Unknown point format {s}"))
        }
    }
}

impl Point {
    fn diff(&self, other: &Self) -> i64 {
        (self.w - other.w).abs()
            + (self.x - other.x).abs()
            + (self.y - other.y).abs()
            + (self.z - other.z).abs()
    }
}

#[derive(Debug, Default)]
struct UnionFind {
    parents: FxHashMap<Point, Point>,
    ranks: FxHashMap<Point, usize>,
}

impl UnionFind {
    fn run(&mut self, points: Vec<Point>) -> usize {
        for n in points.iter() {
            self.parents.insert(n.clone(), n.clone());
            self.ranks.insert(n.clone(), 1);
        }

        let mut components = points.len();
        for i in 0..points.len() {
            for j in i + 1..points.len() {
                let (p1, p2) = (&points[i], &points[j]);
                if p1.diff(p2) <= 3 && self.union(p1, p2) {
                    components -= 1;
                }
            }
        }
        components
    }

    fn union(&mut self, n1: &Point, n2: &Point) -> bool {
        let (p1, p2) = (self.find(n1), self.find(n2));
        if p1 == p2 {
            false
        } else {
            let (r1, r2) = (self.ranks[&p1], self.ranks[&p2]);
            let (parent, child) = if r1 >= r2 { (p1, p2) } else { (p2, p1) };
            *self.ranks.get_mut(&parent).unwrap() += self.ranks[&child];
            self.parents.insert(child, parent);
            true
        }
    }

    fn find<'a>(&'a self, mut n: &'a Point) -> Point {
        while self.parents.get(n).unwrap() != n {
            n = self.parents.get(n).unwrap();
        }
        n.clone()
    }
}

fn main() {
    answer::timer(solution);
}

fn solution() {
    let points = Reader::default().read_from_str();
    let mut union_find = UnionFind::default();
    answer::part1(375, union_find.run(points));
}
