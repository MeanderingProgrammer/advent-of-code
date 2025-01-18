use aoc_lib::answer;
use aoc_lib::assembunny::{Computer, Instruction, Value};
use aoc_lib::reader::Reader;

fn main() {
    answer::timer(solution);
}

fn solution() {
    let instructions = Reader::default().read_from_str();
    answer::part1(318117, run(&instructions, false));
    answer::part2(9227771, run(&instructions, true));
}

fn run(instructions: &[Instruction], ignite: bool) -> i64 {
    let mut computer = Computer::default();
    if ignite {
        computer.set(&Value::Register('c'), &Value::Integer(1));
    }
    computer.run(instructions);
    computer.get(&Value::Register('a'))
}
