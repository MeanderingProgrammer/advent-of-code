use fxhash::FxHashSet;
use priority_queue::DoublePriorityQueue;
use std::collections::VecDeque;
use std::fmt::Debug;
use std::hash::Hash;

pub trait Node: Debug + Clone + Hash + Eq {}
impl<T: Debug + Clone + Hash + Eq> Node for T {}

pub trait Bfs<T: Node> {
    fn done(&self, node: &T) -> bool;

    fn neighbors(&self, node: &T) -> impl Iterator<Item = T>;

    fn run(&self, start: &T) -> Option<i64> {
        let mut queue = VecDeque::new();
        queue.push_back((start.clone(), 0));
        let mut seen = FxHashSet::default();
        while !queue.is_empty() {
            let (node, weight) = queue.pop_front().unwrap();
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

pub trait Dijkstra<T: Node> {
    fn done(&self, node: &T) -> bool;

    fn neighbors(&self, node: &T) -> impl Iterator<Item = (T, i64)>;

    fn run(&self, start: &T) -> Option<i64> {
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
