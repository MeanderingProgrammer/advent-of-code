use aoc_lib::reader::Reader;

#[test]
fn test_group_int() {
    assert_eq!(
        vec![vec![123, 45], vec![-68, -9, 0]],
        reader("group-ints.txt").read_group_int()
    );
}

#[test]
fn test_group_lines() {
    assert_eq!(
        vec![vec!["ab", "cd"], vec!["efg", "hi", "j"]],
        reader("group-strings.txt").read_group_lines()
    );
}

#[test]
fn test_full_groups() {
    assert_eq!(
        vec!["ab\ncd", "efg\nhi\nj"],
        reader("group-strings.txt").read_full_groups()
    );
}

#[test]
fn test_int() {
    assert_eq!(vec![12, -75, 105], reader("int-lines.txt").read_int());
}

#[test]
fn test_lines() {
    assert_eq!(
        vec!["zgsnvdmlfuplrubt", "zztdcqzqddaazdjp"],
        reader("string-lines.txt").read_lines()
    );
}

#[test]
fn test_line() {
    assert_eq!("abcd", reader("string-line.txt").read_line());
}

#[test]
fn test_csv() {
    assert_eq!(vec![1, 5, 9, -12], reader("int-csv.txt").read_csv());
}

#[test]
fn test_chars() {
    assert_eq!(
        vec!['a', 'b', 'c', 'd'],
        reader("string-line.txt").read_chars()
    );
}

fn reader(file: &str) -> Reader {
    Reader::new(format!("test-data/{file}"))
}
