use aoc_lib::answer;
use aoc_lib::assembunny::{Computer, Instruction, Value};
use aoc_lib::reader::Reader;

fn main() {
    answer::timer(solution);
}

fn solution() {
    let instructions = Reader::default().read_from_str();
    answer::part1(198, run(&instructions));
}

fn run(instructions: &[Instruction]) -> i64 {
    let mut i = 0;
    loop {
        let mut computer = Computer::default();
        computer.set(&Value::Register('a'), &Value::Integer(i));
        if computer.run(instructions) {
            return i;
        } else {
            i += 1;
        }
    }
}
