use aoc::Reader;

#[test]
fn test_group_int() {
    let actual = reader("group-ints.txt").groups();
    assert_eq!(vec![vec![123, 45], vec![-68, -9, 0]], actual);
}

#[test]
fn test_group_lines() {
    let actual: Vec<Vec<String>> = reader("group-strings.txt").groups();
    assert_eq!(vec![vec!["ab", "cd"], vec!["efg", "hi", "j"]], actual);
}

#[test]
fn test_full_groups() {
    let actual = reader("group-strings.txt").full_groups();
    assert_eq!(vec!["ab\ncd", "efg\nhi\nj"], actual);
}

#[test]
fn test_int() {
    let actual = reader("int-lines.txt").lines();
    assert_eq!(vec![12, -75, 105], actual);
}

#[test]
fn test_lines() {
    let actual: Vec<String> = reader("string-lines.txt").lines();
    assert_eq!(vec!["zgsnvdmlfuplrubt", "zztdcqzqddaazdjp"], actual);
}

#[test]
fn test_line() {
    let actual: String = reader("string-line.txt").line();
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
