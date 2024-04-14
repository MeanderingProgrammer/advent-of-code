use fxhash::FxHashSet;
use priority_queue::DoublePriorityQueue;
use std::collections::VecDeque;
use std::fmt::Debug;
use std::hash::Hash;

pub trait GraphTraversal {
    type T: Debug + Clone + Hash + Eq;

    fn done(&self, node: &Self::T) -> bool;

    fn neighbors(&self, node: &Self::T) -> impl Iterator<Item = Self::T>;

    fn bfs(&self, start: &Self::T) -> Option<i64> {
        self.run(start, true)
    }

    fn dfs(&self, start: &Self::T) -> Option<i64> {
        self.run(start, false)
    }

    fn run(&self, start: &Self::T, front: bool) -> Option<i64> {
        let mut queue = VecDeque::new();
        queue.push_back((start.clone(), 0));
        let mut seen = FxHashSet::default();
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
                return Some(weight);
            }
            for adjacent in self.neighbors(&node) {
                if !seen.contains(&adjacent) {
                    queue.push_back((adjacent, weight + 1))
                }
            }
        }
        None
    }
}

pub trait Dijkstra {
    type T: Debug + Clone + Hash + Eq;

    fn done(&self, node: &Self::T) -> bool;

    fn neighbors(&self, node: &Self::T) -> impl Iterator<Item = (Self::T, i64)>;

    fn run(&self, start: &Self::T) -> Option<i64> {
        let mut queue = DoublePriorityQueue::new();
        queue.push_decrease(start.clone(), 0);
        let mut seen = FxHashSet::default();
        while !queue.is_empty() {
            let (node, weight) = queue.pop_min().unwrap();
            if seen.contains(&node) {
                continue;
            }
            seen.insert(node.clone());
            if self.done(&node) {
                return Some(weight);
            }
            for (adjacent, cost) in self.neighbors(&node) {
                if !seen.contains(&adjacent) {
                    queue.push_decrease(adjacent, weight + cost);
                }
            }
        }
        None
    }
}
