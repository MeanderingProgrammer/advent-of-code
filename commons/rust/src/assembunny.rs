use crate::{Convert, HashMap};
use std::str::FromStr;

#[derive(Debug)]
pub enum Value {
    Register(char),
    Integer(i64),
}

impl FromStr for Value {
    type Err = String;

    fn from_str(s: &str) -> Result<Self, Self::Err> {
        let ch = Convert::ch(s);
        match ch {
            'a'..='d' => Ok(Self::Register(ch)),
            _ => Ok(Self::Integer(s.parse().unwrap())),
        }
    }
}

#[derive(Debug)]
pub enum Instruction {
    Copy(Value, Value),
    Add(Value, Value),
    Jump(Value, Value),
    Out(Value),
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
            "out" => Ok(Self::Out(parts[1].parse()?)),
            opcode => Err(format!("Invalid opcode: {opcode}")),
        }
    }
}

#[derive(Debug)]
pub struct Computer {
    registers: HashMap<char, i64>,
    outputs: Vec<i64>,
}

impl Default for Computer {
    fn default() -> Self {
        Self {
            registers: ['a', 'b', 'c', 'd'].into_iter().map(|ch| (ch, 0)).collect(),
            outputs: Vec::default(),
        }
    }
}

impl Computer {
    pub fn run(&mut self, instructions: &[Instruction]) -> bool {
        let mut ip = 0;
        let mut success = true;
        while Self::inside(ip, instructions) && success && self.outputs.len() < 100 {
            let instruction = &instructions[ip as usize];
            match self.next(instruction) {
                Some(amount) => ip += amount,
                None => success = false,
            };
        }
        success
    }

    fn inside(ip: i64, instructions: &[Instruction]) -> bool {
        ip >= 0 && ip < instructions.len() as i64
    }

    fn next(&mut self, instruction: &Instruction) -> Option<i64> {
        match instruction {
            Instruction::Copy(x, y) => {
                self.set(y, x);
                Some(1)
            }
            Instruction::Add(x, y) => {
                self.set(x, &Value::Integer(self.get(x) + self.get(y)));
                Some(1)
            }
            Instruction::Jump(x, y) => {
                if self.get(x) != 0 {
                    Some(self.get(y))
                } else {
                    Some(1)
                }
            }
            Instruction::Out(x) => {
                let value = self.get(x);
                if value as usize == self.outputs.len() % 2 {
                    self.outputs.push(value);
                    Some(1)
                } else {
                    None
                }
            }
        }
    }

    pub fn get(&self, value: &Value) -> i64 {
        match value {
            Value::Register(ch) => self.registers[ch],
            Value::Integer(v) => *v,
        }
    }

    pub fn set(&mut self, key: &Value, value: &Value) {
        match key {
            Value::Register(ch) => self.registers.insert(*ch, self.get(value)),
            Value::Integer(_) => unreachable!(),
        };
    }
}
