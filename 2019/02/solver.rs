use aoc_lib::answer;
use aoc_lib::int_code::{Computer, NoopBus};
use aoc_lib::reader;

fn main() {
    answer::timer(solution);
}

fn solution() {
    answer::part1(6627023, run(12, 2));
    answer::part1(4019, get_goal().unwrap());
}

fn run(v1: i64, v2: i64) -> i64 {
    let mut memory = reader::read_csv();
    memory[1] = v1;
    memory[2] = v2;
    let mut computer = Computer::new(NoopBus::new(), memory);
    computer.run();
    computer.get(0)
}

fn get_goal() -> Option<i64> {
    for noun in 0..100 {
        for verb in 0..100 {
            if run(noun, verb) == 19_690_720 {
                return Some(100 * noun + verb);
            }
        }
    }
    None
}
