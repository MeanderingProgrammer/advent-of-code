use aoc::prelude::*;
use rayon::prelude::*;
use std::collections::VecDeque;

#[derive(Debug, Clone)]
struct HashInfo {
    i: usize,
    triple: u8,
    quintuple: Option<u8>,
}

#[derive(Debug)]
struct Hasher {
    prefix: String,
    n: usize,
    batch: usize,
    i: usize,
}

impl Hasher {
    fn new(prefix: &str, n: usize, batch: usize) -> Self {
        assert!(batch.is_multiple_of(8));
        Self {
            prefix: prefix.to_string(),
            n,
            batch,
            i: 0,
        }
    }

    fn next(&mut self) -> VecDeque<HashInfo> {
        let result = (self.i..self.i + self.batch)
            .into_par_iter()
            .step_by(8)
            .flat_map(|i| self.compute(i))
            .collect();
        self.i += self.batch;
        result
    }

    fn compute(&self, start: usize) -> VecDeque<HashInfo> {
        let inputs = std::array::from_fn(|i| format!("{}{}", self.prefix, start + i));
        let mut digests = Md5::from(inputs).compute();
        for _ in 0..(self.n) {
            digests = Md5::from(digests).compute();
        }
        Md5::from(digests)
            .buffers
            .into_iter()
            .enumerate()
            .filter_map(|(i, hash)| {
                let hash = &hash[0..32];
                Self::repeat(hash, 3).map(|triple| HashInfo {
                    i: start + i,
                    triple,
                    quintuple: Self::repeat(hash, 5),
                })
            })
            .collect()
    }

    fn repeat(hash: &[u8], size: usize) -> Option<u8> {
        hash.windows(size).find_map(|window| {
            let first = window[0];
            if window.iter().all(|&ch| ch == first) {
                Some(first)
            } else {
                None
            }
        })
    }
}

fn main() {
    answer::timer(solution);
}

fn solution() {
    let prefix = Reader::default().line::<String>();
    answer::part1(15168, generate(&prefix, 0));
    answer::part2(20864, generate(&prefix, 2_016));
}

fn generate(prefix: &str, n: usize) -> usize {
    let mut hasher = Hasher::new(prefix, n, 1_000);
    let mut hashes = VecDeque::default();
    let mut keys = Vec::default();
    while hashes.is_empty() {
        hashes.append(&mut hasher.next());
    }
    while keys.len() < 64 {
        let hash = hashes.pop_front().unwrap();
        let hash_end = hash.i + 1_000;

        while hasher.i <= hash_end {
            hashes.append(&mut hasher.next());
        }

        for other in hashes.iter() {
            if other.i > hash_end {
                break;
            }
            if other.quintuple == Some(hash.triple) {
                keys.push(hash.i);
                break;
            }
        }
    }
    *keys.last().unwrap()
}
