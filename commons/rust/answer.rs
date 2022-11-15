pub fn part1(expected: i64, result: i64) {
	part(1, expected, result);
}

pub fn part2(expected: i64, result: i64) {
	part(2, expected, result);
}

fn part(part: i64, expected: i64, result: i64) {
	if expected != result {
	    panic!("Part {part} incorrect, expected {expected} but got {result}");
	}
	println!("Part {part}: {result}");
}
