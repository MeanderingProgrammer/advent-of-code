use aoc::{answer, HashMap, Parser, Reader};
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
        let [amount, from, to] = Parser::values(s, " ").unwrap();
        Ok(Self { amount, from, to })
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
    let groups = Reader::default().groups::<String>();

    let arrangement = get_arrangement(&groups[0]);
    let instructions: Vec<Instruction> = groups[1].lines().map(|s| s.parse().unwrap()).collect();

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

fn get_arrangement(s: &str) -> HashMap<usize, Vec<char>> {
    let mut arrangement: HashMap<usize, Vec<char>> = HashMap::default();
    for row in s.lines().rev().skip(1) {
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
