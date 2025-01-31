use aoc_lib::answer;
use aoc_lib::collections::HashMap;
use aoc_lib::reader::Reader;
use std::str::FromStr;

#[derive(Debug)]
struct Instruction {
    amount: usize,
    from: usize,
    to: usize,
}

impl FromStr for Instruction {
    type Err = String;

    fn from_str(s: &str) -> Result<Self, Self::Err> {
        let parts: Vec<&str> = s.split(' ').collect();
        Ok(Self {
            amount: parts[1].parse().unwrap(),
            from: parts[3].parse().unwrap(),
            to: parts[5].parse().unwrap(),
        })
    }
}

impl Instruction {
    fn apply_single(&self, arrangement: &mut HashMap<usize, Vec<char>>) {
        for _ in 0..self.amount {
            let value = arrangement.get_mut(&self.from).unwrap().pop().unwrap();
            arrangement.get_mut(&self.to).unwrap().push(value);
        }
    }

    fn apply_multiple(&self, arrangement: &mut HashMap<usize, Vec<char>>) {
        let mut temp = Vec::default();
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
    answer::timer(solution);
}

fn solution() {
    let groups = Reader::default().read_group_lines();

    let arrangement = get_arrangement(&groups[0]);
    let instructions: Vec<Instruction> = groups[1]
        .iter()
        .map(|raw_value| raw_value.parse().unwrap())
        .collect();

    answer::part1(
        "RNZLFZSJH",
        &get_result(
            arrangement.clone(),
            &instructions,
            Instruction::apply_single,
        ),
    );
    answer::part2(
        "CNSFCGJSM",
        &get_result(
            arrangement.clone(),
            &instructions,
            Instruction::apply_multiple,
        ),
    );
}

fn get_arrangement(raw: &[String]) -> HashMap<usize, Vec<char>> {
    let mut arrangement: HashMap<usize, Vec<char>> = HashMap::default();
    for row in raw.iter().rev().skip(1) {
        let row_chars: Vec<char> = row.chars().collect();
        for (i, index) in (1..row.len()).step_by(4).enumerate() {
            let pile_index = i + 1;
            arrangement.entry(pile_index).or_default();
            let ch = row_chars[index];
            if ch != ' ' {
                arrangement.get_mut(&pile_index).unwrap().push(ch);
            }
        }
    }
    arrangement
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
