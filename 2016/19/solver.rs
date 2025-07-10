use aoc::prelude::*;

fn main() {
    answer::timer(solution);
}

fn solution() {
    let n = Reader::default().line();
    answer::part1(1834903, solve(n, true));
    answer::part2(1420280, solve(n, false));
}

fn solve(n: i64, increment: bool) -> i64 {
    let mut winner = 1;
    for i in 1..=n {
        winner += 1;
        if increment || winner > i / 2 {
            winner += 1;
        }
        if winner > i {
            winner = 1;
        }
    }
    winner
}
