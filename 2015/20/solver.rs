use aoc_lib::answer;
use aoc_lib::reader::Reader;
use std::cmp::min;

fn main() {
    answer::timer(solution);
}

fn solution() {
    let goal = Reader::default().read_int()[0] as usize;
    answer::part1(665280, find_first(goal, false));
    answer::part2(705600, find_first(goal, true));
}

fn find_first(goal: usize, lazy: bool) -> usize {
    let mut houses: Vec<usize> = vec![0; goal / 10];
    for i in 1..houses.len() {
        let last_house = if lazy { i * 50 + 1 } else { houses.len() };
        for house in (i..min(last_house, houses.len())).step_by(i) {
            houses[house] += i * if lazy { 11 } else { 10 };
        }
    }
    houses
        .into_iter()
        .enumerate()
        .filter(|(_, house)| house >= &goal)
        .map(|(i, _)| i)
        .next()
        .unwrap()
}
