use aoc_lib::answer;
use aoc_lib::reader::Reader;
use md5::Context;
use std::sync::atomic::{AtomicBool, AtomicUsize, Ordering};
use std::thread;

#[derive(Debug)]
struct State {
    done: AtomicBool,
    index: AtomicUsize,
    result: AtomicUsize,
}

struct Miner {
    context: Context,
    zeros: usize,
}

impl Miner {
    fn new(prefix: String, zeros: usize) -> Self {
        let mut context = Context::new();
        context.consume(prefix);
        Self { context, zeros }
    }

    fn matches(&self, index: usize) -> bool {
        let mut context = self.context.clone();
        context.consume(index.to_string());
        let digest = context.compute();
        (0..self.zeros).all(|i| {
            let section = digest[i / 2];
            let part = if i % 2 == 0 {
                section >> 4
            } else {
                section & 0xf
            };
            part == 0
        })
    }
}

fn main() {
    answer::timer(solution);
}

fn solution() {
    let prefix = Reader::default().read_line();
    answer::part1(346386, first_index(prefix.clone(), 5));
    answer::part2(9958218, first_index(prefix.clone(), 6));
}

fn first_index(prefix: String, zeros: usize) -> usize {
    let state = State {
        done: AtomicBool::new(false),
        index: AtomicUsize::new(0),
        result: AtomicUsize::new(usize::MAX),
    };
    let miner = Miner::new(prefix, zeros);
    thread::scope(|scope| {
        let threads = thread::available_parallelism().unwrap().get();
        for _ in 0..threads {
            scope.spawn(|| worker(&state, &miner, 1_000));
        }
    });
    state.result.load(Ordering::Relaxed)
}

fn worker(state: &State, miner: &Miner, batch_size: usize) {
    while !state.done.load(Ordering::Relaxed) {
        let start = state.index.fetch_add(batch_size, Ordering::Relaxed);
        for i in start..start + batch_size {
            if miner.matches(i) {
                state.done.store(true, Ordering::Relaxed);
                state.result.fetch_min(i, Ordering::Relaxed);
            }
        }
    }
}
