use aoc_lib::answer;

#[test]
fn test_correct() {
    answer::part1(2, 2);
    answer::part2("abc", "abc");
}

#[test]
#[should_panic]
fn test_incorrect() {
    answer::part1(2, -2);
}
