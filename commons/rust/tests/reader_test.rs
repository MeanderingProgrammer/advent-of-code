use aoc::Reader;

#[test]
fn test_groups() {
    let actual = reader("group-strings.txt").groups::<String>();
    assert_eq!(vec!["ab\ncd", "efg\nhi\nj"], actual);
}

#[test]
fn test_int() {
    let actual = reader("int-lines.txt").lines();
    assert_eq!(vec![12, -75, 105], actual);
}

#[test]
fn test_lines() {
    let actual = reader("string-lines.txt").lines::<String>();
    assert_eq!(vec!["zgsnvdmlfuplrubt", "zztdcqzqddaazdjp"], actual);
}

#[test]
fn test_line() {
    let actual = reader("string-line.txt").line::<String>();
    assert_eq!("abcd", actual);
}

#[test]
fn test_csv() {
    let actual = reader("int-csv.txt").csv();
    assert_eq!(vec![1, 5, 9, -12], actual);
}

#[test]
fn test_chars() {
    let actual = reader("string-line.txt").chars();
    assert_eq!(vec!['a', 'b', 'c', 'd'], actual);
}

fn reader(file: &str) -> Reader {
    Reader::new(format!("test-data/{file}"))
}
