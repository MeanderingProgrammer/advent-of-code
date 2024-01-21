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

impl Cli {
    fn file_path(&self) -> String {
        let (year, day) = Self::get_year_day();
        let file_name = if self.test { "sample.txt" } else { "data.txt" };
        format!("data/{year}/{day}/{file_name}")
    }

    fn get_year_day() -> (String, String) {
        let executable_path = env::current_exe().unwrap();
        let binary_name = executable_path.file_name().unwrap().to_str().unwrap();
        let binary_parts: Vec<&str> = binary_name.split("_").collect();
        (binary_parts[1].into(), binary_parts[2].into())
    }
}

#[derive(Debug)]
pub struct Reader {
    path: String,
}

impl Default for Reader {
    fn default() -> Self {
        Self::new(Cli::parse().file_path())
    }
}

impl Reader {
    pub fn new(path: String) -> Self {
        Self { path }
    }

    pub fn read_group_int(&self) -> Vec<Vec<i64>> {
        self.read_groups(Self::to_int)
    }

    pub fn read_group_lines(&self) -> Vec<Vec<String>> {
        self.read_groups(|item| item.to_string())
    }

    pub fn read_groups<T>(&self, f: fn(&str) -> T) -> Vec<Vec<T>> {
        self.read_lines()
            .split(|line| line.is_empty())
            .map(|group| group.iter().map(|item| f(item)).collect())
            .collect()
    }

    pub fn read_full_groups(&self) -> Vec<String> {
        self.read_lines()
            .split(|line| line.is_empty())
            .map(|group| group.join("\n"))
            .collect()
    }

    pub fn read_grid<T: GridValue>(&self, f: fn(char) -> Option<T>) -> Grid<T> {
        Grid::from_lines(self.read_lines(), |ch| f(ch))
    }

    pub fn read_int(&self) -> Vec<i64> {
        self.read(|line| line.parse::<i64>().unwrap())
    }

    pub fn read_lines(&self) -> Vec<String> {
        self.read(|line| line.to_string())
    }

    pub fn read_line(&self) -> String {
        self.read_lines().remove(0)
    }

    pub fn read_csv(&self) -> Vec<i64> {
        self.read_line().split(",").map(Self::to_int).collect()
    }

    pub fn read_chars(&self) -> Vec<char> {
        self.read_line().chars().collect()
    }

    pub fn read<T>(&self, f: fn(&str) -> T) -> Vec<T> {
        let file = File::open(&self.path).expect(&format!("Could not open: {}", self.path));
        BufReader::new(file)
            .lines()
            .map(|line| f(&line.unwrap()))
            .collect()
    }

    fn to_int(value: &str) -> i64 {
        value.trim().parse().unwrap()
    }
}
