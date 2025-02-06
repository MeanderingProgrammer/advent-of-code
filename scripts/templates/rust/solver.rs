use aoc::{answer, Reader};

fn main() {
    answer::timer(solution);
}

fn solution() {
    let data = Reader::default().lines::<String>();
    println!("{:?}", data);
    answer::part1(1, 1);
    answer::part2(1, 1);
}
