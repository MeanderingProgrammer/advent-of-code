use aoc_lib::answer;
use aoc_lib::reader::Reader;
use itertools::Itertools;
use md5;
use std::sync::atomic::{AtomicBool, AtomicUsize, Ordering};
use std::sync::Mutex;
use std::thread;

#[derive(Debug)]
struct State {
    prefix: String,
    index: AtomicUsize,
    done: AtomicBool,
}

#[derive(Debug, Default)]
struct Password {
    data: Vec<(usize, char)>,
    filled: Vec<u32>,
    result: [char; 8],
}

impl Password {
    fn done(&self) -> bool {
        self.filled.len() == self.result.len()
    }

    fn add(&mut self, i: usize, c1: char, c2: char) {
        self.data.push((i, c1));
        match c1.to_digit(10) {
            None => (),
            Some(index) => {
                if (index as usize) < self.result.len() && !self.filled.contains(&index) {
                    self.filled.push(index);
                    self.result[index as usize] = c2;
                }
            }
        }
    }

    fn part_1(&self) -> String {
        self.data
            .clone()
            .into_iter()
            .sorted()
            .take(self.result.len())
            .map(|(_, ch)| ch)
            .collect()
    }

    fn part_2(&self) -> String {
        self.result.iter().collect()
    }
}

fn main() {
    answer::timer(solution);
}

fn solution() {
    let password = get_password_data(Reader::default().read_line());
    answer::part1("d4cd2ee1", &password.part_1());
    answer::part2("f2c730e5", &password.part_2());
}

fn get_password_data(prefix: String) -> Password {
    let shared = State {
        prefix,
        index: AtomicUsize::new(0),
        done: AtomicBool::new(false),
    };
    let password = Mutex::new(Password::default());
    thread::scope(|scope| {
        let threads = thread::available_parallelism().unwrap().get();
        for _ in 0..threads {
            scope.spawn(|| worker(&shared, &password, 1_000));
        }
    });
    password.into_inner().unwrap()
}

fn worker(state: &State, mutex: &Mutex<Password>, batch_size: usize) {
    while !state.done.load(Ordering::Relaxed) {
        let start = state.index.fetch_add(batch_size, Ordering::Relaxed);
        for i in start..start + batch_size {
            update_password_data(state, mutex, i);
        }
    }
}

fn update_password_data(state: &State, mutex: &Mutex<Password>, i: usize) {
    let hash = format!("{:x}", md5::compute(format!("{}{i}", state.prefix)));
    if &hash[0..5] == "00000" {
        let mut password = mutex.lock().unwrap();
        let mut hash_chars = hash.chars().skip(5);
        password.add(i, hash_chars.next().unwrap(), hash_chars.next().unwrap());
        if password.done() {
            state.done.store(true, Ordering::Relaxed);
        }
    }
}
