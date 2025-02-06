use aoc::{answer, Parser, Reader};

fn main() {
    answer::timer(solution);
}

fn solution() {
    let line: String = Reader::default().line();
    let [row, column] = Parser::values(&line, " ").unwrap();
    let index = get_index(row, column);
    answer::part1(19980801, get_password(index));
}

fn get_index(row: i64, column: i64) -> i64 {
    let mut index = 1;
    (1..row).for_each(|i| index += i);
    (1..column).for_each(|i| index += row + i);
    index
}

fn get_password(n: i64) -> i64 {
    let mut password = 20_151_125;
    (1..n).for_each(|_| {
        password *= 252_533;
        password %= 33_554_393;
    });
    password
}
