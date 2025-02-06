use aoc::{answer, Reader};

fn main() {
    answer::timer(solution);
}

fn solution() {
    let data: Vec<String> = Reader::default().lines();
    println!("{:?}", data);
    answer::part1(1, 1);
    answer::part2(1, 1);
}
