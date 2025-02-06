use aoc::{answer, HashMap, Reader, Str};
use std::str::FromStr;

#[derive(Debug, Clone)]
struct Arrangement {
    values: HashMap<usize, Vec<char>>,
}

impl FromStr for Arrangement {
    type Err = String;

    fn from_str(s: &str) -> Result<Self, Self::Err> {
        let mut values: HashMap<usize, Vec<char>> = HashMap::default();
        for row in s.lines().rev().skip(1) {
            let chars: Vec<char> = row.chars().collect();
            for (i, index) in (1..row.len()).step_by(4).enumerate() {
                let ch = chars[index];
                if ch != ' ' {
                    values.entry(i + 1).or_default().push(ch);
                }
            }
        }
        Ok(Self { values })
    }
}

impl Arrangement {
    fn get(&mut self, key: usize) -> &mut Vec<char> {
        self.values.get_mut(&key).unwrap()
    }
}

#[derive(Debug)]
struct Instruction {
    amount: usize,
    from: usize,
    to: usize,
}

impl FromStr for Instruction {
    type Err = String;

    fn from_str(s: &str) -> Result<Self, Self::Err> {
        let [amount, from, to] = [1, 3, 5].map(|i| Str::nth(s, ' ', i));
        Ok(Self { amount, from, to })
    }
}

impl Instruction {
    fn apply(&self, arrangement: &mut Arrangement, reverse: bool) {
        let from = arrangement.get(self.from);
        let mut buffer = (0..self.amount)
            .map(|_| from.pop().unwrap())
            .collect::<Vec<_>>();
        if reverse {
            buffer.reverse();
        }
        let to = arrangement.get(self.to);
        for value in buffer {
            to.push(value);
        }
    }
}

fn main() {
    answer::timer(solution);
}

fn solution() {
    let groups = Reader::default().groups::<String>();
    let arrangement: Arrangement = groups[0].parse().unwrap();
    let instructions = groups[1]
        .lines()
        .map(|s| s.parse().unwrap())
        .collect::<Vec<_>>();
    answer::part1(
        "RNZLFZSJH",
        &get_result(arrangement.clone(), &instructions, false),
    );
    answer::part2(
        "CNSFCGJSM",
        &get_result(arrangement.clone(), &instructions, true),
    );
}

fn get_result(mut arrangement: Arrangement, instructions: &[Instruction], reverse: bool) -> String {
    instructions.iter().for_each(|instruction| {
        instruction.apply(&mut arrangement, reverse);
    });
    (1..arrangement.values.len() + 1)
        .map(|i| arrangement.values.get(&i).unwrap().last().unwrap())
        .collect()
}
