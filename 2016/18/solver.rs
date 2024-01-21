use aoc_lib::answer;
use aoc_lib::reader::Reader;

fn main() {
    answer::timer(solution);
}

fn solution() {
    let data = Reader::default().read_chars();
    let starting_row: Vec<bool> = data.into_iter().map(|ch| ch == '.').collect();
    answer::part1(2013, total_safe(starting_row.clone(), 40));
    answer::part2(20006289, total_safe(starting_row.clone(), 400_000));
}

fn total_safe(starting_row: Vec<bool>, rounds: usize) -> usize {
    let mut safe = 0;
    let mut row = starting_row;
    for _ in 0..rounds {
        safe += row.iter().filter(|&&v| v).count();
        row = next_row(&row);
    }
    safe
}

fn next_row(row: &Vec<bool>) -> Vec<bool> {
    let mut result = Vec::new();
    for i in 0..row.len() {
        let element = get_element(
            *row.get(i - 1).unwrap_or(&true),
            *row.get(i + 1).unwrap_or(&true),
        );
        result.push(element);
    }
    result
}

fn get_element(left: bool, right: bool) -> bool {
    /*
     * Raw conditions for a TRAP can be summed up as an or of:
     * 1)  L &  C & ~R
     * 2) ~L &  C &  R
     * 3)  L & ~C & ~R
     * 4) ~L & ~C &  R
     *
     * Doing some simple grouping we learn that the center value plays no role:
     * (L & C & ~R) | (L & ~C & ~R) -> L & (C | ~C) & ~R -> L & ~R
     * (~L & C & R) | (~L & ~C & R) -> ~L & (C | ~C) & R -> ~L & R
     *
     * Further simplifies to an exclusive or, i.e. not equal (one true one false)
     * (L & ~R) | (~L & R) -> L ^ R
     * This makes the condition for SAFE the opposite, i.e. L == R
     */
    left == right
}
