use aoc_lib::answer;
use aoc_lib::grid::Grid;
use aoc_lib::point::Point;
use aoc_lib::reader::Reader;
use fxhash::FxHashMap;
use rayon::prelude::*;
use std::collections::VecDeque;

#[derive(Debug)]
struct Race {
    grid: Grid<char>,
    start: Point,
    finish: Point,
    distances: FxHashMap<Point, usize>,
    previous: FxHashMap<Point, Point>,
}

impl Race {
    fn new(mut grid: Grid<char>) -> Self {
        let start = grid.get_values('S')[0].clone();
        let finish = grid.get_values('E')[0].clone();
        grid.add(start.clone(), '.');
        grid.add(finish.clone(), '.');
        Self {
            grid,
            start,
            finish,
            distances: FxHashMap::default(),
            previous: FxHashMap::default(),
        }
    }

    fn solve(&mut self) {
        let mut queue = VecDeque::new();
        queue.push_back((self.finish.clone(), 0));
        while !queue.is_empty() {
            let (current, distance) = queue.pop_front().unwrap();
            if self.has_better(&current, distance) {
                continue;
            }
            self.distances.insert(current.clone(), distance);
            for next in current.neighbors().into_iter() {
                let next_distance = distance + 1;
                if self.grid.get(&next) != &'.' {
                    continue;
                }
                if !self.has_better(&next, next_distance) {
                    self.distances.insert(next.clone(), next_distance);
                    self.previous.insert(next.clone(), current.clone());
                    queue.push_back((next, next_distance));
                }
            }
        }
    }

    fn has_better(&self, point: &Point, distance: usize) -> bool {
        return self.distances.contains_key(point)
            && self.distances.get(point).unwrap() < &distance;
    }

    fn cheats(&self, savings: usize, duration: usize) -> usize {
        self.get_path()
            .par_iter()
            .enumerate()
            .map(|(i, point)| self.count_better(savings, duration, i, point))
            .sum()
    }

    fn get_path(&self) -> Vec<Point> {
        let mut result = Vec::default();
        let mut current = self.start.clone();
        while current != self.finish {
            result.push(current.clone());
            current = self.previous.get(&current).unwrap().clone();
        }
        result
    }

    fn count_better(&self, savings: usize, duration: usize, i: usize, point: &Point) -> usize {
        let base_time = self.distances.get(&self.start).unwrap();
        let mut result = 0;
        for x in Self::range_start(point.x, duration)..=Self::range_end(point.x, duration) {
            for y in Self::range_start(point.y, duration)..=Self::range_end(point.y, duration) {
                let option = Point::new(x as i64, y as i64);
                let distance = point.manhattan_distance(&option) as usize;
                if distance < 2 || distance > duration {
                    continue;
                }
                if !self.grid.contains(&option) || self.grid.get(&option) != &'.' {
                    continue;
                }
                let cheat_time = i + distance + self.distances.get(&option).unwrap();
                if &cheat_time >= base_time {
                    continue;
                }
                let saved = base_time - cheat_time;
                if saved >= savings {
                    result += 1;
                }
            }
        }
        result
    }

    fn range_start(value: i64, offset: usize) -> usize {
        let v = value as usize;
        if offset >= v {
            0
        } else {
            v - offset
        }
    }

    fn range_end(value: i64, offset: usize) -> usize {
        let v = value as usize;
        v + offset
    }
}

fn main() {
    answer::timer(solution);
}

fn solution() {
    let grid = Reader::default().read_grid(Some);
    let mut race = Race::new(grid);
    race.solve();
    answer::part1(1399, race.cheats(100, 2));
    answer::part2(994807, race.cheats(100, 20));
}