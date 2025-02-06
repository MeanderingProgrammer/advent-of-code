use aoc::{answer, Md5, Reader};
use std::sync::atomic::{AtomicBool, AtomicUsize, Ordering};
use std::thread;

#[derive(Debug)]
struct State {
    done: AtomicBool,
    index: AtomicUsize,
    result: AtomicUsize,
}

struct Miner {
    prefix: String,
    mask: u32,
}

impl Miner {
    fn new(prefix: String, zeros: usize) -> Self {
        assert!(zeros <= 8);
        let mask = !((1 << (32 - (4 * zeros))) - 1);
        Self { prefix, mask }
    }

    fn matches(&self, index: usize) -> Option<usize> {
        let inputs = std::array::from_fn(|i| format!("{}{}", self.prefix, index + i));
        let digests = Md5::from(inputs).compute();
        digests
            .into_iter()
            .enumerate()
            .filter(|(_, [digest, _, _, _])| *digest & self.mask == 0)
            .map(|(i, _)| index + i)
            .next()
    }
}

fn main() {
    answer::timer(solution);
}

fn solution() {
    let prefix = Reader::default().line::<String>();
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
        for i in (start..start + batch_size).step_by(8) {
            if let Some(i) = miner.matches(i) {
                state.done.store(true, Ordering::Relaxed);
                state.result.fetch_min(i, Ordering::Relaxed);
            }
        }
    }
}
