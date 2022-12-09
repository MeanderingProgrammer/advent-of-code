use std::fs::File;
use std::io::{BufRead, BufReader};

const TEST: bool = false;

pub fn read_int() -> Vec<i64> {
    read(|line| line.parse::<i64>().unwrap())
}

pub fn read_lines() -> Vec<String> {
    read(|line| line.to_string())
}

pub fn read_chars() -> Vec<char> {
    read_lines()[0].chars().collect()
}

pub fn read<T>(f: fn(&str) -> T) -> Vec<T> {
    let file_name = if TEST { "sample.txt" } else { "data.txt" };
    let reader = File::open(file_name)
        .map(|file| BufReader::new(file))
        .expect(&format!("could not open '{}'", file_name));

    reader.lines()
        .map(|line| f(&line.unwrap()))
        .collect()
}
