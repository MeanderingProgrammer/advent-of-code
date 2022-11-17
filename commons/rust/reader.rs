use std::fs::File;
use std::io::{BufRead, BufReader};


pub fn read_int() -> Vec<i64> {
    read(|line| line.parse::<i64>().unwrap())
}

fn read<T>(f: fn(String) -> T) -> Vec<T> {
    let reader = File::open("data.txt")
        .map(|file| BufReader::new(file))
        .expect("could not open 'data.txt'");

    reader.lines()
        .map(|line| f(line.unwrap()))
        .collect()
}
