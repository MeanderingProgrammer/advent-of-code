use std::fmt::Display;
use std::cmp::PartialEq;


pub trait Solution: Display + PartialEq {}
impl<T: Display + PartialEq> Solution for T {}

pub fn part1<T: Solution>(expected: T, result: T) {
	part(1, expected, result);
}

pub fn part2<T: Solution>(expected: T, result: T) {
	part(2, expected, result);
}

fn part<T: Solution>(part: i64, expected: T, result: T) {
	if expected != result {
	    panic!("Part {part} incorrect, expected {expected} but got {result}");
	}
	println!("Part {part}: {result}");
}
