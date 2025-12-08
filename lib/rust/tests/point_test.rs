use aoc::prelude::*;
use std::collections::HashSet;
use std::str::FromStr;

#[test]
fn test_str() {
    let point = Point::new(17, -5);
    assert_eq!(Ok(point.clone()), "17,-5".parse());
    assert_eq!(Ok(point.clone()), " 17 , -5 ".parse());
    assert_eq!(Ok(point.clone()), "<17 , -5>".parse());
    assert_eq!(Ok(point.clone()), "<x=17 , y=-5>".parse());
    assert_eq!(Ok(point.clone()), "prefix <x=17 , y=-5>".parse());
    assert!(Point::from_str("17,-5,0").is_err());
    assert_eq!("(17, -5)", point.to_string());
}

#[test]
fn test_str_3d() {
    let point = Point3d::new(-1, 0, 102);
    assert_eq!(Ok(point.clone()), "-1,0,102".parse());
    assert_eq!(Ok(point.clone()), " -1, 0, 102 ".parse());
    assert_eq!(Ok(point.clone()), "<-1, 0, 102>".parse());
    assert_eq!(Ok(point.clone()), "<x=-1, y=0, z=102>".parse());
    assert_eq!(Ok(point.clone()), "prefix <x=-1, y=0, z=102>".parse());
    assert!(Point3d::from_str("-1,0,102,0").is_err());
    assert_eq!("(-1, 0, 102)", point.to_string());
}

#[test]
fn test_math() {
    let point = Point::new(1, 2);
    assert_eq!(Point::new(-3, 6), point.add(Point::new(-4, 4)));
    assert_eq!(Point::new(1, 1), point.add(&Direction::Up));
    assert_eq!(Point::new(2, 1), point.add(&Heading::NorthEast));
    assert_eq!(Point::new(-5, -10), point.mul(-5));
}

#[test]
fn test_math_3d() {
    let point = Point3d::new(1, 0, 5);
    assert_eq!(Point3d::new(-3, 4, 7), point.add(Point3d::new(-4, 4, 2)));
    assert_eq!(Point3d::new(1, 0, 6), point.add(&Direction3d::Up));
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
    assert_eq!(
        HashSet::from([
            Point::new(-1, 2),
            Point::new(-1, 4),
            Point::new(0, 3),
            Point::new(-2, 3),
            Point::new(-2, 2),
            Point::new(-2, 4),
            Point::new(0, 2),
            Point::new(0, 4),
        ]),
        p.all_neighbors().into_iter().collect(),
    );
}

#[test]
fn test_neighbors_3d() {
    let p = Point3d::new(-1, 3, 4);
    assert_eq!(
        HashSet::from([
            Point3d::new(-1, 2, 4),
            Point3d::new(-1, 4, 4),
            Point3d::new(0, 3, 4),
            Point3d::new(-2, 3, 4),
            Point3d::new(-1, 3, 3),
            Point3d::new(-1, 3, 5),
        ]),
        p.neighbors().into_iter().collect(),
    );
}

#[test]
fn test_distance() {
    assert_eq!(5.0, Point::new(0, 0).euclidean(&Point::new(3, 4)));
    assert_eq!(7, Point::new(0, 0).manhattan(&Point::new(3, 4)));
    assert_eq!(9, Point::new(-2, 7).length());
}

#[test]
fn test_distance_3d() {
    assert_eq!(13, Point3d::new(-2, 7, -4).length());
}
