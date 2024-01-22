use aoc_lib::answer;
use aoc_lib::reader::Reader;
use nom::{
    bytes::complete::{tag, take},
    character::complete::{alphanumeric1, digit1, newline},
    combinator::map_res,
    multi::separated_list1,
    sequence::tuple,
    IResult,
};
use std::str::FromStr;

#[derive(Debug)]
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

#[derive(Debug)]
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

#[derive(Debug)]
struct Monkey {
    items: Vec<i64>,
    operation: (Operator, Value),
    divisible_by: i64,
    true_monkey: usize,
    false_monkey: usize,
    inspections: i64,
}

impl Monkey {
    fn from_str(input: &str) -> IResult<&str, Self> {
        // Monkey 0:
        //  Starting items: 97, 81, 57, 57, 91, 61
        //  Operation: new = old * 7
        //  Test: divisible by 11
        //    If true: throw to monkey 5
        //    If false: throw to monkey 6

        let (input, _) = tuple((tag("Monkey "), digit1, tag(":"), newline))(input)?;
        let (input, items) = tuple((
            tag("  Starting items: "),
            separated_list1(tag(", "), map_res(digit1, |s: &str| s.parse())),
            newline,
        ))(input)?;
        let (input, operation) = tuple((
            tag("  Operation: new = old "),
            map_res(take(1usize), |s: &str| s.parse()),
            tag(" "),
            map_res(alphanumeric1, |s: &str| s.parse()),
            newline,
        ))(input)?;
        let (input, divisible_by) = tuple((
            tag("  Test: divisible by "),
            map_res(digit1, |s: &str| s.parse()),
            newline,
        ))(input)?;
        let (input, true_monkey) = tuple((
            tag("    If true: throw to monkey "),
            map_res(digit1, |s: &str| s.parse()),
            newline,
        ))(input)?;
        let (input, false_monkey) = tuple((
            tag("    If false: throw to monkey "),
            map_res(digit1, |s: &str| s.parse()),
        ))(input)?;

        Ok((
            input,
            Self {
                items: items.1,
                operation: (operation.1, operation.3),
                divisible_by: divisible_by.1,
                true_monkey: true_monkey.1,
                false_monkey: false_monkey.1,
                inspections: 0,
            },
        ))
    }

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
    answer::part1(56350, monkey_business(20, true));
    answer::part2(13954061248, monkey_business(10_000, false));
}

fn monkey_business(rounds: usize, reduce_worry: bool) -> i64 {
    let mut monkeys: Vec<Monkey> = Reader::default()
        .read_full_groups()
        .iter()
        .map(|group| Monkey::from_str(group).unwrap().1)
        .collect();

    // This can be the least common multiple, but doesn't need to be to work
    let mut multiple_of_all = 1;
    for monkey in &monkeys {
        multiple_of_all *= monkey.divisible_by;
    }

    for _ in 0..rounds {
        for m in 0..monkeys.len() {
            let monkey = &mut monkeys[m];

            let mut movements: Vec<ItemMove> = Vec::new();
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
