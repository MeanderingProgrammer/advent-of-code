use aoc::prelude::*;

#[derive(Debug)]
struct Rectangle {
    x: (i32, i32),
    y: (i32, i32),
}

impl Rectangle {
    fn new(a: &Point, b: &Point) -> Self {
        let x = (a.x.min(b.x), a.x.max(b.x));
        let y = (a.y.min(b.y), a.y.max(b.y));
        assert!(x.0 <= x.1 && y.0 <= y.1);
        Self { x, y }
    }

    fn area(&self) -> usize {
        let dx = (self.x.0 - self.x.1).unsigned_abs() as usize;
        let dy = (self.y.0 - self.y.1).unsigned_abs() as usize;
        (dx + 1) * (dy + 1)
    }

    fn inner(&self) -> Option<Self> {
        let x = (self.x.0 + 1, self.x.1 - 1);
        let y = (self.y.0 + 1, self.y.1 - 1);
        if x.0 <= x.1 && y.0 <= y.1 {
            Some(Self { x, y })
        } else {
            None
        }
    }

    fn overlaps(&self, other: &Self) -> bool {
        let x = self.x.0.max(other.x.0) <= self.x.1.min(other.x.1);
        let y = self.y.0.max(other.y.0) <= self.y.1.min(other.y.1);
        x && y
    }
}

#[derive(Debug)]
struct Polygon {
    lines: Vec<Rectangle>,
}

impl Polygon {
    fn new(points: &[Point]) -> Self {
        let mut lines = Vec::new();
        for i in 0..points.len() {
            let p1 = &points[i];
            let p2 = &points[(i + 1) % points.len()];
            lines.push(Rectangle::new(p1, p2));
        }
        Self { lines }
    }

    fn contains(&self, rectangle: &Rectangle) -> bool {
        // does not handle corners of rectangle being outside of polygon as those
        // do not produce a large enough area to worry about for this puzzle
        // the same thing applies to single line rectangles
        match rectangle.inner() {
            Some(inner) => !self.lines.iter().any(|line| line.overlaps(&inner)),
            None => false,
        }
    }
}

fn main() {
    answer::timer(solution);
}

fn solution() {
    let points = Reader::default().lines::<Point>();
    let polygon = Polygon::new(&points);
    answer::part1(4759420470, max_area(&points, &polygon, false));
    answer::part2(1603439684, max_area(&points, &polygon, true));
}

fn max_area(points: &[Point], polygon: &Polygon, check: bool) -> usize {
    (0..points.len())
        .flat_map(|i| (i + 1..points.len()).map(move |j| (i, j)))
        .filter_map(|(i, j)| {
            let rectangle = Rectangle::new(&points[i], &points[j]);
            if !check || polygon.contains(&rectangle) {
                Some(rectangle.area())
            } else {
                None
            }
        })
        .max()
        .unwrap()
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_area() {
        let rectangle = Rectangle::new(&Point::new(1, 1), &Point::new(3, 5));
        assert_eq!(15, rectangle.area());
    }

    #[test]
    fn test_polygon() {
        // ...#XX#..#XX#...
        // ...X..X..X..X...
        // ...X..X..X..X...
        // #XX#..#XX#..#XX#
        // X..............X
        // X..............X
        // #XX#..#XX#..#XX#
        // ...#XX#..#XX#...
        let polygon = Polygon::new(&[
            Point::new(0, 3),
            Point::new(3, 3),
            Point::new(3, 0),
            Point::new(6, 0),
            Point::new(6, 3),
            Point::new(9, 3),
            Point::new(9, 0),
            Point::new(12, 0),
            Point::new(12, 3),
            Point::new(15, 3),
            Point::new(15, 6),
            Point::new(12, 6),
            Point::new(12, 7),
            Point::new(9, 7),
            Point::new(9, 6),
            Point::new(6, 6),
            Point::new(6, 7),
            Point::new(3, 7),
            Point::new(3, 6),
            Point::new(0, 6),
        ]);
        let data = [
            ((0, 3), (3, 0), true),  // wrong due to corners
            ((0, 3), (3, 3), false), // wrong due to single line
            ((0, 3), (15, 6), true),
            ((0, 3), (12, 7), false),
            ((3, 0), (6, 3), true),
            ((3, 0), (6, 6), true),
            ((3, 0), (6, 7), true),
            ((3, 0), (9, 3), false),
            ((3, 0), (12, 3), false),
            ((3, 0), (12, 6), false),
            ((3, 0), (12, 7), false),
            ((0, 6), (15, 6), false),
        ];
        for ((x1, y1), (x2, y2), expected) in data {
            let (a, b) = (Point::new(x1, y1), Point::new(x2, y2));
            let rectangle = Rectangle::new(&a, &b);
            assert_eq!(expected, polygon.contains(&rectangle))
        }
    }
}
