use aoc_lib::answer;
use aoc_lib::reader;

#[derive(Debug)]
struct Monkey {
    items: Vec<i64>,
    expression: String,
    divisible_by: i64,
    true_monkey: usize,
    false_monkey: usize,
    inspections: i64,
}

impl Monkey {
    fn apply_operation(&self, item: i64) -> i64 {
        let parts: Vec<&str> = self.expression.split(" ").collect();
        let v2 = match parts[2] {
            "old" => item,
            num => num.parse::<i64>().unwrap(),
        };
        match parts[1] {
            "+" => item + v2,
            "*" => item * v2,
            _ => unreachable!(),
        }
    }
}

#[derive(Debug)]
struct ItemMove {
    item: i64,
    to: usize,
}

fn main() {
    answer::part1(56350, get_monkey_business(20, true));
    answer::part2(13954061248, get_monkey_business(10_000, false));
}

fn get_monkey_business(rounds: usize, reduce_worry: bool) -> i64 {
    let mut monkeys = get_monkeys();

    // This can be the least common multiple, but doesn't need to be to work
    let mut multiple_of_all = 1;
    for monkey in &monkeys {
        multiple_of_all *= monkey.divisible_by;
    }

    for _ in 0..rounds {
        for m in 0..monkeys.len() {
            let monkey = &mut monkeys[m];

            let mut movements: Vec<ItemMove> = Vec::new();
            while monkey.items.len() > 0 {
                let mut item = monkey.items.remove(0);
                item = monkey.apply_operation(item);
                item = if reduce_worry { item / 3 } else { item };
                item = item % multiple_of_all;

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

fn get_monkeys() -> Vec<Monkey> {
    reader::read_group_lines()
        .iter()
        .map(|group| Monkey {
            items: group[1]
                .split_once(": ")
                .unwrap()
                .1
                .split(", ")
                .map(|item| item.parse::<i64>().unwrap())
                .collect(),
            expression: group[2].split_once(" = ").unwrap().1.to_string(),
            divisible_by: group[3].split(" ").last().unwrap().parse::<i64>().unwrap(),
            true_monkey: group[4]
                .split(" ")
                .last()
                .unwrap()
                .parse::<usize>()
                .unwrap(),
            false_monkey: group[5]
                .split(" ")
                .last()
                .unwrap()
                .parse::<usize>()
                .unwrap(),
            inspections: 0,
        })
        .collect()
}
