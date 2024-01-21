use aoc_lib::answer;
use aoc_lib::reader::Reader;

fn main() {
    answer::timer(solution);
}

fn solution() {
    let data = Reader::default().read_lines();
    println!("{:?}", data);
    answer::part1(1, 1);
}
