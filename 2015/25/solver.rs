use aoc_lib::answer;
use aoc_lib::reader::Reader;
use nom::{bytes::complete::tag, character::complete::digit0, IResult};

fn main() {
    answer::timer(solution);
}

fn solution() {
    let line = Reader::default().read_line();
    let (row, column) = parse_line(&line).unwrap().1;
    let index = get_index(row, column);
    answer::part1(19980801, get_password(index));
}

fn parse_line(input: &str) -> IResult<&str, (i64, i64)> {
    let (input, _) = tag("To continue, please consult the code grid in the manual.  ")(input)?;
    let (input, _) = tag("Enter the code at row ")(input)?;
    let (input, row) = digit0(input)?;
    let (input, _) = tag(", column ")(input)?;
    let (input, column) = digit0(input)?;
    let (input, _) = tag(".")(input)?;
    Ok((input, (row.parse().unwrap(), column.parse().unwrap())))
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
