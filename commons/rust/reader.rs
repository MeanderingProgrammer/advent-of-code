use crate::grid::Grid;
use crate::point::Point;
use std::fs::File;
use std::io::{BufRead, BufReader};

const TEST: bool = false;

pub fn read_group_int() -> Vec<Vec<i64>> {
    read_groups(|item| item.parse::<i64>().unwrap())
}

pub fn read_group_lines() -> Vec<Vec<String>> {
    read_groups(|item| item.to_string())
}

fn read_groups<T>(f: fn(&str) -> T) -> Vec<Vec<T>> {
    read_lines()
        .split(|line| line.is_empty())
        .map(|group| group.iter().map(|item| f(item)).collect())
        .collect()
}

pub fn read_grid() -> Grid<i64> {
    let mut grid: Grid<i64> = Grid::new();
    for (y, line) in read_lines().iter().enumerate() {
        for (x, ch) in line.char_indices() {
            grid.add(
                Point::new_2d(x as i64, y as i64), 
                ch.to_digit(10).unwrap() as i64,
            );
        }
    }
    grid
}

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
