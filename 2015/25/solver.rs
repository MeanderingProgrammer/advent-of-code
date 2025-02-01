use aoc::{answer, Reader};

fn main() {
    answer::timer(solution);
}

fn solution() {
    let line = Reader::default().read_line();
    let (row, column) = parse_line(&line);
    let index = get_index(row, column);
    answer::part1(19980801, get_password(index));
}

fn parse_line(s: &str) -> (i64, i64) {
    let words: Vec<&str> = s.split_whitespace().collect();
    let (row, column) = (words[words.len() - 3], words[words.len() - 1]);
    (
        row[..row.len() - 1].parse().unwrap(),
        column[..column.len() - 1].parse().unwrap(),
    )
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
