use std::fmt::Debug;
use std::time::Instant;

pub fn timer(solution: fn() -> ()) {
    let start = Instant::now();
    solution();
    println!("Runtime (ns): {}", start.elapsed().as_nanos());
}

pub trait Solution: Debug + PartialEq + ToString {}
impl<T: Debug + PartialEq + ToString> Solution for T {}

pub fn part1<T: Solution>(expected: T, result: T) {
    part(1, expected, result);
}

pub fn part2<T: Solution>(expected: T, result: T) {
    part(2, expected, result);
}

fn part<T: Solution>(part: i64, expected: T, result: T) {
    if expected != result {
        panic!(
            "Part {part} incorrect, expected {0} but got {1}",
            expected.to_string(),
            result.to_string(),
        );
    }
    println!("Part {part}: {0}", result.to_string());
}
