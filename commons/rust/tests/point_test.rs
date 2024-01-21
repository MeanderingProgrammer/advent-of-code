use aoc_lib::point::{Direction, Heading, Point};
use std::collections::HashSet;

#[test]
fn test_math() {
    assert_eq!(Point::new(-3, 6), &Point::new(1, 2) + &Point::new(-4, 4));
    assert_eq!(Point::new(1, 1), &Point::new(1, 2) + &Direction::Up);
    assert_eq!(Point::new(2, 1), &Point::new(1, 2) + &Heading::NorthEast);
    assert_eq!(Point::new(-5, -10), &Point::new(1, 2) * -5);
}

#[test]
fn test_neighbors() {
    let p = Point::new(-1, 3);
    assert_eq!(
        HashSet::from([
            Point::new(-1, 2),
            Point::new(-1, 4),
            Point::new(0, 3),
            Point::new(-2, 3),
        ]),
        p.neighbors().into_iter().collect(),
    );
}
