use crate::queue::{HeapVariant, PriorityQueue};
use fxhash::FxHashSet;
use std::collections::VecDeque;
use std::fmt::Debug;
use std::hash::Hash;

pub trait GraphSearch {
    type T: Debug + Clone + Hash + Eq;

    fn first(&self) -> bool;

    fn done(&self, node: &Self::T) -> bool;

    fn neighbors(&self, node: &Self::T) -> impl Iterator<Item = Self::T>;

    fn bfs(&self, start: Self::T) -> Vec<i64> {
        self.run(start, true)
    }

    fn dfs(&self, start: Self::T) -> Vec<i64> {
        self.run(start, false)
    }

    fn run(&self, start: Self::T, front: bool) -> Vec<i64> {
        let mut queue = VecDeque::new();
        queue.push_back((start, 0));
        let mut seen = FxHashSet::default();
        let mut result = Vec::default();
        while !queue.is_empty() {
            // Remove from either the front (BFS) or back (DFS)
            let (node, weight) = if front {
                queue.pop_front().unwrap()
            } else {
                queue.pop_back().unwrap()
            };
            if seen.contains(&node) {
                continue;
            }
            seen.insert(node.clone());
            if self.done(&node) {
                result.push(weight);
                if self.first() {
                    break;
                }
            } else {
                for adjacent in self.neighbors(&node) {
                    if !seen.contains(&adjacent) {
                        queue.push_back((adjacent, weight + 1))
                    }
                }
            }
        }
        result
    }
}

pub trait Dijkstra {
    type T: Debug + Clone + Hash + Eq;

    fn done(&self, node: &Self::T) -> bool;

    fn neighbors(&self, node: &Self::T) -> impl Iterator<Item = (Self::T, i64)>;

    fn run(&self, start: Self::T) -> Option<i64> {
        let mut queue = PriorityQueue::new(HeapVariant::Min);
        queue.push(start, 0);
        let mut seen = FxHashSet::default();
        while !queue.is_empty() {
            let (node, weight) = queue.pop().unwrap();

            if seen.contains(&node) {
                continue;
            }
            seen.insert(node.clone());

            if self.done(&node) {
                return Some(weight);
            }
            for (adjacent, cost) in self.neighbors(&node) {
                if !seen.contains(&adjacent) {
                    queue.push(adjacent, weight + cost);
                }
            }
        }
        None
    }
}
