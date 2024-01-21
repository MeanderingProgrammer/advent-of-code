use aoc_lib::reader::Reader;
use std::io::Write;
use tempfile::NamedTempFile;

#[test]
fn test_group_int() {
    assert_eq!(
        vec![vec![123, 45], vec![-68, -9, 0]],
        reader(&new_file(&["123", "45", "", "-68", "-9", "0"])).read_group_int()
    );
}

#[test]
fn test_group_lines() {
    assert_eq!(
        vec![vec!["ab", "cd"], vec!["efg", "hi", "j"]],
        reader(&new_file(&["ab", "cd", "", "efg", "hi", "j"])).read_group_lines()
    );
}

#[test]
fn test_full_groups() {
    assert_eq!(
        vec!["ab\ncd", "efg\nhi\nj"],
        reader(&new_file(&["ab", "cd", "", "efg", "hi", "j"])).read_full_groups()
    );
}

#[test]
fn test_int() {
    assert_eq!(
        vec![12, -75, 105],
        reader(&new_file(&["12", "-75", "105"])).read_int()
    );
}

#[test]
fn test_lines() {
    let lines = vec!["zgsnvdmlfuplrubt", "zztdcqzqddaazdjp"];
    assert_eq!(lines, reader(&new_file(&lines)).read_lines());
}

#[test]
fn test_line() {
    assert_eq!("abcd", reader(&new_file(&["abcd"])).read_line());
}

#[test]
fn test_csv() {
    assert_eq!(
        vec![1, 5, 9, -12],
        reader(&new_file(&["1,5,9,-12"])).read_csv()
    );
}

#[test]
fn test_chars() {
    assert_eq!(
        vec!['a', 'b', 'c', 'd'],
        reader(&new_file(&["abcd"])).read_chars()
    );
}

fn new_file(lines: &[&str]) -> NamedTempFile {
    let mut file = NamedTempFile::new().unwrap();
    for line in lines {
        writeln!(file, "{line}").unwrap();
    }
    file
}

fn reader(file: &NamedTempFile) -> Reader {
    Reader::new(file.path().to_str().unwrap().to_string())
}
