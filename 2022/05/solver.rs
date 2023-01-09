use aoc_lib::answer;
use aoc_lib::reader;
use std::collections::HashMap;

#[derive(Debug)]
struct Instruction {
    amount: usize,
    from: usize,
    to: usize,
}

impl Instruction {
    fn apply_single(&self, arrangement: &mut HashMap<usize, Vec<char>>) {
        for _ in 0..self.amount {
            let value = arrangement.get_mut(&self.from).unwrap().pop().unwrap();
            arrangement.get_mut(&self.to).unwrap().push(value);
        }
    }

    fn apply_multiple(&self, arrangement: &mut HashMap<usize, Vec<char>>) {
        let mut temp = Vec::new();
        for _ in 0..self.amount {
            let value = arrangement.get_mut(&self.from).unwrap().pop().unwrap();
            temp.push(value);
        }
        temp.iter().rev().for_each(|value| {
            arrangement.get_mut(&self.to).unwrap().push(*value);
        });
    }
}

fn main() {
    let lines = reader::read_lines();
    let arrangement_instructions: Vec<&[String]> = lines.split(|line| line.is_empty()).collect();

    let arrangement = get_arrangement(arrangement_instructions[0]);
    let instructions = get_instructions(arrangement_instructions[1]);

    answer::part1("RNZLFZSJH", &get_result(arrangement.clone(), &instructions, |instruction, arr| {
        instruction.apply_single(arr);
    }));
    answer::part2("CNSFCGJSM", &get_result(arrangement.clone(), &instructions, |instruction, arr| {
        instruction.apply_multiple(arr);
    }));
}

fn get_arrangement(raw: &[String]) -> HashMap<usize, Vec<char>> {
    let mut arrangement: HashMap<usize, Vec<char>> = HashMap::new();
    for row in raw.iter().rev().skip(1) {
        let row_chars: Vec<char> = row.chars().collect();
        for (i, index) in (1..row.len()).step_by(4).enumerate() {
            let pile_index = i + 1;
            if !arrangement.contains_key(&pile_index) {
                arrangement.insert(pile_index, Vec::new());
            }
            let ch = row_chars[index];
            if ch != ' ' {
                arrangement.get_mut(&pile_index).unwrap().push(ch);
            }
        }
    }
    arrangement
}

fn get_instructions(raw: &[String]) -> Vec<Instruction> {
    raw.iter()
        .map(|raw_value| {
            let parts: Vec<&str> = raw_value.split(" ").collect();
            Instruction {
                amount: parts[1].parse::<usize>().unwrap(),
                from: parts[3].parse::<usize>().unwrap(),
                to: parts[5].parse::<usize>().unwrap(),
            }
        })
        .collect()
}

fn get_result(
    mut arrangement: HashMap<usize, Vec<char>>,
    instructions: &[Instruction],
    f: fn(&Instruction, &mut HashMap<usize, Vec<char>>) -> (),
) -> String {
    instructions.iter().for_each(|instruction| {
        f(instruction, &mut arrangement);
    });
    (1..arrangement.len() + 1)
        .map(|i| arrangement.get(&i).unwrap().last().unwrap())
        .collect()
}
