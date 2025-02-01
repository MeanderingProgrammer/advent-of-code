use aoc::{answer, Reader};

fn main() {
    answer::timer(solution);
}

fn solution() {
    let snafu_numbers = Reader::default().read_lines();
    let total_fuel: i64 = snafu_numbers
        .iter()
        .map(|snafu_number| to_decimal(snafu_number))
        .sum();
    answer::part1("2011-=2=-1020-1===-1", &to_snafu(total_fuel));
}

fn to_decimal(snafu: &str) -> i64 {
    let mut result = 0;
    snafu.chars().for_each(|ch| {
        result *= 5;
        result += match ch {
            '2' => 2,
            '1' => 1,
            '0' => 0,
            '-' => -1,
            '=' => -2,
            _ => unreachable!(),
        };
    });
    result
}

fn to_snafu(decimal: i64) -> String {
    let mut result = "".to_string();
    let mut target = decimal;
    while target != 0 {
        let (value, carry) = match target % 5 {
            0 => ('0', 0),
            1 => ('1', 0),
            2 => ('2', 0),
            // 3 = 5 - 2
            3 => ('=', 1),
            // 4 = 5 - 1
            4 => ('-', 1),
            _ => unreachable!(),
        };
        result.insert(0, value);
        target /= 5;
        target += carry;
    }
    result
}
