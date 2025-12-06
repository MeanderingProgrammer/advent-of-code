use std::fmt::Debug;
use std::time::Instant;

pub fn timer(solution: fn() -> ()) {
    let start = Instant::now();
    solution();
    println!("Runtime (ns): {}", start.elapsed().as_nanos());
}

pub trait Solution: Debug + PartialEq + ToString {}
impl<T: Debug + PartialEq + ToString> Solution for T {}

pub fn part1<T: Solution>(expected: T, actual: T) {
    part(1, expected, actual);
}

pub fn part2<T: Solution>(expected: T, actual: T) {
    part(2, expected, actual);
}

fn part<T: Solution>(part: i64, expected: T, actual: T) {
    if expected != actual {
        panic!(
            "Part {part}: expected {0} got {1}",
            expected.to_string(),
            actual.to_string(),
        );
    }
    println!("Part {part}: {0}", actual.to_string());
}
