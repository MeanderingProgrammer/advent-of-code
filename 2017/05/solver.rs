use aoc_lib::answer;
use aoc_lib::reader;

fn main() {
    answer::part1(373160, run(|v| v + 1));
    answer::part2(26395586, run(|v| if v >= 3 { v - 1 } else { v + 1 }));
}

fn run(f: fn(i64) -> i64) -> usize {
    let mut jumps = reader::read_int();
    let mut steps = 0;
    let mut ip: i64 = 0;
    while ip >= 0 && ip < jumps.len() as i64 {
        let jump = jumps[ip as usize];
        jumps[ip as usize] = f(jump);
        ip += jump;
        steps += 1;
    }
    steps
}
