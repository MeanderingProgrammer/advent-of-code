use aoc::{answer, Iter, Md5, Reader};
use std::fmt::Write;
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
    data: Vec<(usize, u8)>,
    filled: Vec<u8>,
    result: [u8; 8],
}

impl Password {
    fn done(&self) -> bool {
        self.filled.len() == self.result.len()
    }

    fn add(&mut self, i: usize, c1: u8, c2: u8) {
        self.data.push((i, c1));
        if (c1 as usize) < self.result.len() && !self.filled.contains(&c1) {
            self.filled.push(c1);
            self.result[c1 as usize] = c2;
        }
    }

    fn part_1(&self) -> Vec<u8> {
        self.data
            .iter()
            .sorted()
            .take(self.result.len())
            .map(|(_, ch)| *ch)
            .collect()
    }

    fn part_2(&self) -> Vec<u8> {
        self.result.to_vec()
    }
}

fn main() {
    answer::timer(solution);
}

fn solution() {
    let password = get_password(Reader::default().read_line());
    answer::part1("d4cd2ee1", &to_hex(&password.part_1()));
    answer::part2("f2c730e5", &to_hex(&password.part_2()));
}

fn get_password(prefix: String) -> Password {
    let state = State {
        prefix,
        index: AtomicUsize::new(0),
        done: AtomicBool::new(false),
    };
    let password = Mutex::new(Password::default());
    thread::scope(|scope| {
        let threads = thread::available_parallelism().unwrap().get();
        for _ in 0..threads {
            scope.spawn(|| worker(&state, &password, 1_000));
        }
    });
    password.into_inner().unwrap()
}

fn worker(state: &State, mutex: &Mutex<Password>, batch_size: usize) {
    while !state.done.load(Ordering::Relaxed) {
        let start = state.index.fetch_add(batch_size, Ordering::Relaxed);
        for i in (start..start + batch_size).step_by(8) {
            update_password(state, mutex, i);
        }
    }
}

fn update_password(state: &State, mutex: &Mutex<Password>, start: usize) {
    let inputs = std::array::from_fn(|i| format!("{}{}", state.prefix, start + i));
    let digests = Md5::from(inputs).compute();
    for (i, digest) in digests.into_iter().enumerate() {
        // Equivalent to first 5 hex characters == "00000"
        if digest[0] == 0 && digest[1] == 0 && digest[2] < 16 {
            // Retrieve characters 6 & 7
            let (c1, c2) = (digest[2], digest[3] >> 4);
            let mut password = mutex.lock().unwrap();
            password.add(start + i, c1, c2);
            if password.done() {
                state.done.store(true, Ordering::Relaxed);
            }
        }
    }
}

fn to_hex(chars: &[u8]) -> String {
    let mut result = String::default();
    chars
        .iter()
        .for_each(|ch| write!(result, "{:x}", ch).unwrap());
    result
}
