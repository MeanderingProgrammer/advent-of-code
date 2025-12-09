use aoc::prelude::*;

#[derive(Debug)]
struct Edge {
    value: i32,
    min: i32,
    max: i32,
}

impl Edge {
    fn new(value: i32, a: i32, b: i32) -> Self {
        Self {
            value,
            min: a.min(b),
            max: a.max(b),
        }
    }

    fn contains(&self, value: i32) -> bool {
        value >= self.min && value <= self.max
    }

    fn crosses(&self, other: &Self) -> bool {
        self.value > other.min
            && self.value < other.max
            && other.value > self.min
            && other.value < self.max
    }
}

#[derive(Debug)]
struct Polygon {
    points: Vec<Point>,
    hedges: Vec<Edge>,
    vedges: Vec<Edge>,
}

impl Polygon {
    fn new(points: &[Point]) -> Self {
        let mut hedges = Vec::new();
        let mut vedges = Vec::new();
        for i in 0..points.len() {
            let p1 = &points[i];
            let p2 = &points[(i + 1) % points.len()];
            if p1.y == p2.y {
                assert_ne!(p1.x, p2.x);
                hedges.push(Edge::new(p1.y, p1.x, p2.x));
            } else {
                vedges.push(Edge::new(p1.x, p1.y, p2.y));
            }
        }
        Self {
            points: points.to_vec(),
            hedges,
            vedges,
        }
    }

    fn contains(&self, p1: &Point, p2: &Point) -> bool {
        let (l, r) = (p1.x.min(p2.x), p1.x.max(p2.x));
        let (t, b) = (p1.y.min(p2.y), p1.y.max(p2.y));

        if self
            .points
            .iter()
            .any(|c| c.x > l && c.x < r && c.y > t && c.y < b)
        {
            return false;
        }

        if self.outside(Point::new(l, t))
            || self.outside(Point::new(r, t))
            || self.outside(Point::new(l, b))
            || self.outside(Point::new(r, b))
        {
            return false;
        }

        if self
            .hedges
            .iter()
            .any(|e| e.crosses(&Edge::new(l, t, b)) || e.crosses(&Edge::new(r, t, b)))
        {
            return false;
        }

        if self
            .vedges
            .iter()
            .any(|e| e.crosses(&Edge::new(t, l, r)) || e.crosses(&Edge::new(b, l, r)))
        {
            return false;
        }

        true
    }

    fn outside(&self, p: Point) -> bool {
        let mut left = 0;
        let mut right = 0;
        let mut crossed = 0;
        for edge in &self.hedges {
            if edge.value == p.y {
                if edge.contains(p.x) {
                    return false;
                }
            } else if edge.value > p.y {
                if p.x == edge.max {
                    assert!(edge.min < p.x);
                    left += 1;
                    if left == right {
                        crossed += 1;
                    }
                } else if p.x == edge.min {
                    assert!(edge.max > p.x);
                    right += 1;
                    if left == right {
                        crossed += 1;
                    }
                } else if edge.contains(p.x) {
                    crossed += 1;
                }
            }
        }
        crossed % 2 == 0
    }
}

fn main() {
    answer::timer(solution);
}

fn solution() {
    let points = Reader::default().lines::<Point>();

    let polygon = Polygon::new(&points);

    let pairs = (0..points.len())
        .flat_map(|i| (i + 1..points.len()).map(move |j| (i, j)))
        .collect::<Vec<_>>();

    let mut part1 = 0;
    for (i, j) in &pairs {
        part1 = part1.max(area(&points[*i], &points[*j]));
    }

    let mut part2 = 0;
    for (i, j) in &pairs {
        let p1 = &points[*i];
        let p2 = &points[*j];
        if polygon.contains(p1, p2) {
            part2 = part2.max(area(p1, p2));
        }
    }

    answer::part1(4759420470, part1);
    answer::part2(1603439684, part2);
}

fn area(a: &Point, b: &Point) -> usize {
    let dx = (a.x - b.x).unsigned_abs() as usize;
    let dy = (a.y - b.y).unsigned_abs() as usize;
    (dx + 1) * (dy + 1)
}
