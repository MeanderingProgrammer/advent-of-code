use aoc::prelude::*;
use std::fmt::Debug;
use std::fs::File;
use std::io::Write;
use tempfile::tempdir;

#[test]
fn test_chars() {
    validate(&["abcd"], |reader| reader.chars(), vec!['a', 'b', 'c', 'd']);
}

#[test]
fn test_csv() {
    validate(&["1,5,9,-12"], |reader| reader.csv(), vec![1, 5, 9, -12]);
}

#[test]
fn test_groups() {
    validate(
        &["ab", "cd", "", "efg", "hi", "j"],
        |reader| reader.groups(),
        vec!["ab\ncd".to_string(), "efg\nhi\nj".to_string()],
    );
}

#[test]
fn test_line() {
    validate(&["abcd"], |reader| reader.line(), "abcd".to_string());
}

#[test]
fn test_lines_string() {
    validate(
        &["abcd", "efgh"],
        |reader| reader.lines(),
        vec!["abcd".to_string(), "efgh".to_string()],
    );
}

#[test]
fn test_lines_int() {
    validate(
        &["12", "-75", "105"],
        |reader| reader.lines(),
        vec![12, -75, 105],
    );
}

fn validate<T>(lines: &[&str], f: fn(Reader) -> T, expected: T)
where
    T: Debug + PartialEq,
{
    let dir = tempdir().unwrap();
    let path = dir.path().join("data.txt");
    let mut file = File::create(&path).unwrap();
    for line in lines {
        writeln!(file, "{}", line).unwrap();
    }
    let actual = f(Reader::new(path));
    assert_eq!(expected, actual);
}
