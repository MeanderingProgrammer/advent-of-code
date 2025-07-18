use crate::prelude::*;
use std::env;
use std::fmt::Debug;
use std::fs::File;
use std::io::{BufRead, BufReader};
use std::str::FromStr;

#[derive(Debug)]
struct Cli<'a> {
    file_name: &'a str,
}

impl Cli<'_> {
    fn parse() -> Self {
        let test = match env::args().nth(1) {
            None => false,
            Some(value) => value == "--test",
        };
        Self {
            file_name: if test { "sample.txt" } else { "data.txt" },
        }
    }

    fn file_path(&self) -> String {
        let (year, day) = Self::get_year_day();
        format!("data/{year}/{day}/{}", self.file_name)
    }

    fn get_year_day() -> (String, String) {
        let path = env::current_exe().unwrap();
        let binary = path.file_name().unwrap().to_str().unwrap();
        let parts: Vec<&str> = binary.split('_').collect();
        (parts[1].into(), parts[2].into())
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

    pub fn grid<T: FromChar>(&self) -> Grid<T> {
        (&self.lines::<String>()).into()
    }

    pub fn chars<T: FromChar>(&self) -> Vec<T> {
        self.line::<String>()
            .chars()
            .map(|ch| T::from_char(ch).unwrap())
            .collect()
    }

    pub fn csv<T>(&self) -> Vec<T>
    where
        T: FromStr,
        T::Err: Debug,
    {
        self.line::<String>()
            .split(',')
            .map(|s| s.parse().unwrap())
            .collect()
    }

    pub fn groups<T>(&self) -> Vec<T>
    where
        T: FromStr,
        T::Err: Debug,
    {
        self.lines::<String>()
            .split(|line| line.is_empty())
            .map(|lines| lines.join("\n").parse().unwrap())
            .collect()
    }

    pub fn line<T>(&self) -> T
    where
        T: FromStr,
        T::Err: Debug,
    {
        self.lines().remove(0)
    }

    pub fn lines<T>(&self) -> Vec<T>
    where
        T: FromStr,
        T::Err: Debug,
    {
        match File::open(&self.path) {
            Ok(file) => BufReader::new(file)
                .lines()
                .map(|s| s.unwrap().parse().unwrap())
                .collect(),
            Err(_) => panic!("Could not open: {}", self.path),
        }
    }
}
