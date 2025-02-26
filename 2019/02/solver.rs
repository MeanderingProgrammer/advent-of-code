use aoc::int_code::{Computer, NoopBus};
use aoc::{Reader, answer};

fn main() {
    answer::timer(solution);
}

fn solution() {
    let memory = Reader::default().csv();
    answer::part1(6627023, run(&memory, 12, 2));
    answer::part2(4019, get_goal(&memory).unwrap());
}

fn run(memory: &[i64], v1: i64, v2: i64) -> i64 {
    let mut memory = memory.to_vec();
    memory[1] = v1;
    memory[2] = v2;
    let mut computer: Computer<NoopBus> = Computer::default(&memory);
    computer.run();
    computer.get(0)
}

fn get_goal(memory: &[i64]) -> Option<i64> {
    for noun in 0..100 {
        for verb in 0..100 {
            if run(memory, noun, verb) == 19_690_720 {
                return Some(100 * noun + verb);
            }
        }
    }
    None
}
