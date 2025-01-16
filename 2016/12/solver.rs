use aoc_lib::answer;
use aoc_lib::reader::Reader;
use fxhash::FxHashMap;
use std::str::FromStr;

#[derive(Debug)]
enum Value {
    Register(char),
    Integer(i64),
}

impl FromStr for Value {
    type Err = String;

    fn from_str(s: &str) -> Result<Self, Self::Err> {
        let ch = s.chars().next().unwrap();
        match ch {
            'a'..='d' => Ok(Self::Register(ch)),
            _ => Ok(Self::Integer(s.parse().unwrap())),
        }
    }
}

#[derive(Debug)]
enum Instruction {
    Copy(Value, Value),
    Add(Value, Value),
    Jump(Value, Value),
}

impl FromStr for Instruction {
    type Err = String;

    fn from_str(s: &str) -> Result<Self, Self::Err> {
        let parts: Vec<&str> = s.split_whitespace().collect();
        match parts[0] {
            "cpy" => Ok(Self::Copy(parts[1].parse()?, parts[2].parse()?)),
            "inc" => Ok(Self::Add(parts[1].parse()?, "1".parse()?)),
            "dec" => Ok(Self::Add(parts[1].parse()?, "-1".parse()?)),
            "jnz" => Ok(Self::Jump(parts[1].parse()?, parts[2].parse()?)),
            opcode => Err(format!("Invalid opcode: {opcode}")),
        }
    }
}

#[derive(Debug)]
struct Computer {
    registers: FxHashMap<char, i64>,
}

impl Default for Computer {
    fn default() -> Self {
        Self {
            registers: ['a', 'b', 'c', 'd'].into_iter().map(|ch| (ch, 0)).collect(),
        }
    }
}

impl Computer {
    fn run(&mut self, instructions: &[Instruction]) {
        let mut ip: i64 = 0;
        while ip >= 0 && ip < instructions.len() as i64 {
            let instruction = &instructions[ip as usize];
            ip += self.next(instruction).unwrap_or(1);
        }
    }

    fn next(&mut self, instruction: &Instruction) -> Option<i64> {
        match instruction {
            Instruction::Copy(x, y) => {
                self.set(y, x);
                None
            }
            Instruction::Add(x, y) => {
                self.set(x, &Value::Integer(self.get(x) + self.get(y)));
                None
            }
            Instruction::Jump(x, y) => {
                if self.get(x) != 0 {
                    Some(self.get(y))
                } else {
                    None
                }
            }
        }
    }

    fn get(&self, value: &Value) -> i64 {
        match value {
            Value::Register(ch) => self.registers[ch],
            Value::Integer(v) => *v,
        }
    }

    fn set(&mut self, key: &Value, value: &Value) {
        match key {
            Value::Register(ch) => self.registers.insert(*ch, self.get(value)),
            Value::Integer(_) => unreachable!(),
        };
    }
}

fn main() {
    answer::timer(solution);
}

fn solution() {
    let instructions: Vec<Instruction> = Reader::default().read_from_str();
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
