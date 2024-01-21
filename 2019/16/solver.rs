use aoc_lib::answer;
use aoc_lib::reader::Reader;

#[derive(Debug)]
struct Transmission {
    digits: Vec<i64>,
}

impl Transmission {
    fn new(digits: &String) -> Self {
        Self {
            digits: digits
                .chars()
                .map(|ch| ch.to_digit(10).unwrap() as i64)
                .collect(),
        }
    }

    fn standard(&mut self) {
        let mut new_digits = Vec::new();
        for i in 0..self.digits.len() {
            new_digits.push(self.standard_digit(i));
        }
        self.digits = new_digits;
    }

    fn standard_digit(&self, i: usize) -> i64 {
        let mut pattern_index = 0;
        let mut new_digit = 0;
        self.digits.iter().for_each(|digit| {
            pattern_index += 1;
            new_digit += [0, 1, 0, -1][(pattern_index / (i + 1)) % 4] * digit;
        });
        new_digit.abs() % 10
    }

    fn offset(&mut self) {
        // Going from back to front each digit is the current sum % 10
        // This only applies in the middle of a set of digits and does not hold to the start
        let mut new_digits = Vec::new();
        let mut current_sum = 0;
        for digit in self.digits.iter().rev() {
            current_sum += digit;
            new_digits.push(current_sum % 10);
        }
        new_digits.reverse();
        self.digits = new_digits;
    }

    fn to_string(&self) -> String {
        self.digits.iter().map(|digit| digit.to_string()).collect()
    }
}

fn main() {
    answer::timer(solution);
}

fn solution() {
    answer::part1(77038830, apply_fft(1, false));
    answer::part2(28135104, apply_fft(10_000, true));
}

fn apply_fft(repeats: usize, apply_offset: bool) -> usize {
    let lines = Reader::default().read_lines();
    let line = lines.first().unwrap();
    let mut digits = line.repeat(repeats);
    if apply_offset {
        digits = digits[first_n(&digits, 7)..].to_string();
    }
    let mut transmission = Transmission::new(&digits);
    for _ in 0..100 {
        if apply_offset {
            transmission.offset();
        } else {
            transmission.standard();
        }
    }
    first_n(&transmission.to_string(), 8)
}

fn first_n(digits: &String, n: usize) -> usize {
    let substring = &digits[..n];
    substring.parse().unwrap()
}
