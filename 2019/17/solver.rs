use aoc::int_code::{Bus, Computer};
use aoc::{answer, Direction, Point, Reader};
use std::collections::VecDeque;

#[derive(Debug)]
enum Turn {
    Left,
    Right,
}

impl Turn {
    fn code(&self) -> String {
        match self {
            Self::Left => "L".to_string(),
            Self::Right => "R".to_string(),
        }
    }
}

#[derive(Debug, Clone)]
struct DroidState {
    location: Point,
    direction: Direction,
}

impl DroidState {
    fn get_instructions(&mut self, scaffolding: &[Point]) -> Vec<String> {
        let mut instructions = Vec::default();
        let mut turn = self.get_turn(scaffolding);
        while let Some(current) = turn {
            self.direction = match current {
                Turn::Left => self.direction.left(),
                Turn::Right => self.direction.right(),
            };
            let amount = self.move_until_end(scaffolding);
            instructions.push(format!("{},{}", current.code(), amount));
            turn = self.get_turn(scaffolding);
        }
        instructions
    }

    fn get_turn(&self, scaffolding: &[Point]) -> Option<Turn> {
        if scaffolding.contains(&self.go(Some(Turn::Left))) {
            Some(Turn::Left)
        } else if scaffolding.contains(&self.go(Some(Turn::Right))) {
            Some(Turn::Right)
        } else {
            None
        }
    }

    fn move_until_end(&mut self, scaffolding: &[Point]) -> usize {
        let mut amount = 0;
        while scaffolding.contains(&self.go(None)) {
            self.location = self.go(None);
            amount += 1;
        }
        amount
    }

    fn go(&self, turn: Option<Turn>) -> Point {
        let direction = match turn {
            None => &self.direction,
            Some(Turn::Left) => &self.direction.left(),
            Some(Turn::Right) => &self.direction.right(),
        };
        self.location.add(direction)
    }
}

#[derive(Debug, Clone)]
struct Instruction {
    function: Vec<String>,
    starts: Vec<usize>,
}

impl Instruction {
    fn contains(&self, i: usize) -> bool {
        self.starts
            .iter()
            .any(|&start| i >= start && i < start + self.function.len())
    }

    fn get_end(&self, i: usize) -> Option<usize> {
        self.starts.iter().find_map(|&start| {
            if i == start {
                Some(start + self.function.len())
            } else {
                None
            }
        })
    }
}

#[derive(Debug, Clone)]
struct Compressed {
    routine: Vec<String>,
    a_function: Vec<String>,
    b_function: Vec<String>,
    c_function: Vec<String>,
}

#[derive(Debug, Clone)]
struct Compression {
    instructions: Vec<String>,
    max_length: usize,
}

impl Compression {
    fn compress(&self) -> Compressed {
        let (a, b, c) = self.compress_instructions().unwrap();
        Compressed {
            routine: self.create_routine(vec![("A", &a), ("B", &b), ("C", &c)]),
            a_function: a.function,
            b_function: b.function,
            c_function: c.function,
        }
    }

    fn compress_instructions(&self) -> Option<(Instruction, Instruction, Instruction)> {
        for a in self.generate_instructions(vec![]) {
            for b in self.generate_instructions(vec![&a]) {
                for c in self.generate_instructions(vec![&a, &b]) {
                    if self.first_out(vec![&a, &b, &c]).is_none() {
                        return Some((a, b, c));
                    }
                }
            }
        }
        None
    }

    fn generate_instructions(&self, previous: Vec<&Instruction>) -> Vec<Instruction> {
        let start = self.first_out(previous).unwrap();
        (1..=self.max_length)
            .map(|i| {
                let function = self.instructions[start..start + i].to_vec();
                Instruction {
                    function: function.clone(),
                    starts: self.get_starts(&function),
                }
            })
            .collect()
    }

    fn get_starts(&self, function: &Vec<String>) -> Vec<usize> {
        let mut bounds = vec![];
        let mut i = 0;
        while i < self.instructions.len() - function.len() + 1 {
            if &self.instructions[i..i + function.len()] == function.as_slice() {
                bounds.push(i);
                i += function.len();
            } else {
                i += 1;
            }
        }
        bounds
    }

    fn first_out(&self, instructions: Vec<&Instruction>) -> Option<usize> {
        (0..self.instructions.len()).find(|&i| {
            !instructions
                .iter()
                .any(|instruction| instruction.contains(i))
        })
    }

    fn create_routine(&self, name_instruction: Vec<(&str, &Instruction)>) -> Vec<String> {
        let mut routine = vec![];
        let mut i = 0;
        while i < self.instructions.len() {
            let (name, end) = name_instruction
                .iter()
                .map(|(name, instruction)| (name, instruction.get_end(i)))
                .filter(|(_, end)| end.is_some())
                .map(|(name, end)| (name, end.unwrap()))
                .next()
                .unwrap();
            routine.push(name.to_string());
            i = end;
        }
        routine
    }
}

#[derive(Debug, Default)]
struct VacuumDroid {
    current: Point,
    scaffolding: Vec<Point>,
    instructions: VecDeque<char>,
    state: Option<DroidState>,
    running: bool,
    value: Option<i64>,
}

impl Bus for VacuumDroid {
    fn active(&self) -> bool {
        true
    }

    fn get_input(&mut self) -> i64 {
        self.instructions.pop_front().unwrap() as i64
    }

    fn add_output(&mut self, value: i64) {
        if self.running {
            self.value = Some(value);
        } else {
            self.current = self.update_scaffolding(char::from_u32(value as u32).unwrap());
        }
    }
}

impl VacuumDroid {
    fn update_scaffolding(&mut self, value: char) -> Point {
        match value {
            '\n' => Point::new(0, self.current.y + 1),
            '.' => self.current.add(&Direction::Right),
            '#' => {
                self.scaffolding.push(self.current.clone());
                self.current.add(&Direction::Right)
            }
            value => {
                self.state = Some(DroidState {
                    location: self.current.clone(),
                    direction: value.to_string().parse().unwrap(),
                });
                self.scaffolding.push(self.current.clone());
                self.current.add(&Direction::Right)
            }
        }
    }

    fn dust_collect(&self) -> i32 {
        self.scaffolding
            .iter()
            .filter(|point| self.is_intersection(point))
            .map(|point| point.x * point.y)
            .sum()
    }

    fn is_intersection(&self, point: &Point) -> bool {
        point
            .neighbors()
            .iter()
            .all(|neighbor| self.scaffolding.contains(neighbor))
    }

    fn create_path(&mut self) {
        self.running = true;
        let mut state = self.state.clone().unwrap();
        let compressed = Compression {
            instructions: state.get_instructions(&self.scaffolding),
            max_length: 5,
        }
        .compress();
        self.add_instruction(&compressed.routine);
        self.add_instruction(&compressed.a_function);
        self.add_instruction(&compressed.b_function);
        self.add_instruction(&compressed.c_function);
        self.add_instruction(&["n".to_string()]);
    }

    fn add_instruction(&mut self, instructions: &[String]) {
        let as_string = instructions.join(",") + "\n";
        self.instructions.append(&mut as_string.chars().collect());
    }
}

fn main() {
    answer::timer(solution);
}

fn solution() {
    let memory = Reader::default().read_csv();
    let droid = VacuumDroid::default();
    let mut droid = run_droid(&memory, droid, false);
    droid.create_path();
    let droid = run_droid(&memory, droid, true);
    answer::part1(9876, droid.dust_collect());
    answer::part2(1234055, droid.value.unwrap());
}

fn run_droid(memory: &[i64], droid: VacuumDroid, prompt: bool) -> VacuumDroid {
    let mut memory = memory.to_vec();
    memory[0] = if prompt { 2 } else { memory[0] };
    let mut computer = Computer::new(droid, &memory);
    computer.run();
    computer.bus
}
