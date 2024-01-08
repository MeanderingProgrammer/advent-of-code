use crate::grid::{Grid, GridValue};
use clap::Parser;
use std::env;
use std::fs::File;
use std::io::{BufRead, BufReader};

#[derive(Debug, Parser)]
struct Cli {
    #[clap(long, short, action)]
    test: bool,
}

pub fn read_group_int() -> Vec<Vec<i64>> {
    read_groups(|item| to_int(item))
}

pub fn read_group_lines() -> Vec<Vec<String>> {
    read_groups(|item| item.to_string())
}

pub fn read_groups<T>(f: fn(&str) -> T) -> Vec<Vec<T>> {
    read_lines()
        .split(|line| line.is_empty())
        .map(|group| group.iter().map(|item| f(item)).collect())
        .collect()
}

pub fn read_full_groups() -> Vec<String> {
    read_lines()
        .split(|line| line.is_empty())
        .map(|group| group.join("\n"))
        .collect()
}

pub fn read_grid<T: GridValue>(f: fn(char) -> Option<T>) -> Grid<T> {
    Grid::from_lines(read_lines(), |ch| f(ch))
}

pub fn read_int() -> Vec<i64> {
    read(|line| line.parse::<i64>().unwrap())
}

pub fn read_lines() -> Vec<String> {
    read(|line| line.to_string())
}

pub fn read_line() -> String {
    read_lines().remove(0)
}

pub fn read_csv() -> Vec<i64> {
    read_line().split(",").map(|value| to_int(value)).collect()
}

pub fn read_chars() -> Vec<char> {
    read_line().chars().collect()
}

fn to_int(value: &str) -> i64 {
    value.trim().parse().unwrap()
}

pub fn read<T>(f: fn(&str) -> T) -> Vec<T> {
    let (year, day) = get_year_day();
    let args = Cli::parse();
    let file_name = if args.test { "sample.txt" } else { "data.txt" };
    let reader = File::open(format!("data/{year}/{day}/{file_name}"))
        .map(|file| BufReader::new(file))
        .expect(&format!("could not open '{}'", file_name));
    reader.lines().map(|line| f(&line.unwrap())).collect()
}

fn get_year_day() -> (String, String) {
    let executable_path = env::current_exe().unwrap();
    let binary_name = executable_path.file_name().unwrap().to_str().unwrap();
    let binary_parts: Vec<&str> = binary_name.split("_").collect();
    (binary_parts[1].into(), binary_parts[2].into())
}
