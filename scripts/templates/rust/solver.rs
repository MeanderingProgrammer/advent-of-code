use aoc_lib::answer;
use aoc_lib::reader;

fn main() {
    answer::timer(solution);
}

fn solution() {
    let data = reader::read_lines();
    println!("{:?}", data);
    answer::part1(1, 1);
}
