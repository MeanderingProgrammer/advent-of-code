use aoc::prelude::*;
use std::str::FromStr;

#[derive(Debug, Clone)]
enum Operator {
    Add,
    Multiply,
}

impl FromStr for Operator {
    type Err = String;

    fn from_str(s: &str) -> Result<Self, Self::Err> {
        match s {
            "+" => Ok(Self::Add),
            "*" => Ok(Self::Multiply),
            _ => Err("Unknown operator".to_string()),
        }
    }
}

#[derive(Debug, Clone)]
enum Value {
    Old,
    Number(i64),
}

impl FromStr for Value {
    type Err = String;

    fn from_str(s: &str) -> Result<Self, Self::Err> {
        match s {
            "old" => Ok(Self::Old),
            num => Ok(Self::Number(num.parse().unwrap())),
        }
    }
}

#[derive(Debug, Clone)]
struct Monkey {
    items: Vec<i64>,
    operation: (Operator, Value),
    divisible_by: i64,
    true_monkey: usize,
    false_monkey: usize,
    inspections: i64,
}

impl FromStr for Monkey {
    type Err = String;

    fn from_str(s: &str) -> Result<Self, Self::Err> {
        // Monkey 0:
        //  Starting items: 97, 81, 57, 57, 91, 61
        //  Operation: new = old * 7
        //  Test: divisible by 11
        //    If true: throw to monkey 5
        //    If false: throw to monkey 6

        let lines: Vec<&str> = s.lines().collect();
        let (_, items) = lines[1].split_once(": ").unwrap();
        let [true_monkey, false_monkey] = [lines[4], lines[5]].map(|s| Str::nth_rev(s, ' ', 0));
        Ok(Self {
            items: items
                .split(", ")
                .map(|item| item.parse().unwrap())
                .collect(),
            operation: (
                Str::nth_rev(lines[2], ' ', 1),
                Str::nth_rev(lines[2], ' ', 0),
            ),
            divisible_by: Str::nth_rev(lines[3], ' ', 0),
            true_monkey,
            false_monkey,
            inspections: 0,
        })
    }
}

impl Monkey {
    fn apply_operation(&self, item: i64) -> i64 {
        let v2 = match self.operation.1 {
            Value::Old => item,
            Value::Number(num) => num,
        };
        match self.operation.0 {
            Operator::Add => item + v2,
            Operator::Multiply => item * v2,
        }
    }
}

#[derive(Debug)]
struct ItemMove {
    item: i64,
    to: usize,
}

fn main() {
    answer::timer(solution);
}

fn solution() {
    let monkeys = Reader::default().groups();
    answer::part1(56350, monkey_business(monkeys.clone(), 20, true));
    answer::part2(13954061248, monkey_business(monkeys.clone(), 10_000, false));
}

fn monkey_business(mut monkeys: Vec<Monkey>, rounds: usize, reduce_worry: bool) -> i64 {
    // This can be the least common multiple, but doesn't need to be to work
    let mut multiple_of_all = 1;
    for monkey in &monkeys {
        multiple_of_all *= monkey.divisible_by;
    }

    for _ in 0..rounds {
        for m in 0..monkeys.len() {
            let monkey = &mut monkeys[m];

            let mut movements: Vec<ItemMove> = Vec::default();
            while !monkey.items.is_empty() {
                let mut item = monkey.items.remove(0);
                item = monkey.apply_operation(item);
                item = if reduce_worry { item / 3 } else { item };
                item %= multiple_of_all;

                monkey.inspections += 1;

                movements.push(ItemMove {
                    item,
                    to: if item % monkey.divisible_by == 0 {
                        monkey.true_monkey
                    } else {
                        monkey.false_monkey
                    },
                });
            }

            movements
                .iter()
                .for_each(|movement| monkeys[movement.to].items.push(movement.item));
        }
    }

    let mut inspections: Vec<i64> = monkeys.iter().map(|monkey| monkey.inspections).collect();
    inspections.sort();
    inspections.reverse();

    inspections[0] * inspections[1]
}
