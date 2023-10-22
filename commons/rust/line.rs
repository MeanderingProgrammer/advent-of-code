use crate::point::Point;

#[derive(Debug)]
pub struct Line2d {
    p1: Point,
    p2: Point,
}

impl Line2d {
    pub fn new(p1: Point, p2: Point) -> Self {
        if p1.dimensions() != 2 || p1.dimensions() != 2 {
            panic!("Only 2 dimensional points supported");
        }
        Line2d { p1, p2 }
    }

    pub fn as_points(&self) -> Vec<Point> {
        if self.p1.x() != self.p2.x() && self.p2.y() != self.p2.y() {
            panic!("Lines must be either horizontal or vertical");
        }

        let (x1, x2) = (self.p1.x(), self.p2.x());
        let (y1, y2) = (self.p1.y(), self.p2.y());

        (x1.min(x2)..=x1.max(x2))
            .flat_map(move |x| (y1.min(y2)..=y1.max(y2)).map(move |y| Point::new_2d(x, y)))
            .collect()
    }
}
