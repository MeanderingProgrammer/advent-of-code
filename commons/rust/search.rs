use priority_queue::DoublePriorityQueue;
use std::collections::HashSet;
use std::fmt::Debug;
use std::hash::Hash;

pub trait Node: Debug + Clone + Hash + Eq {}
impl<T: Debug + Clone + Hash + Eq> Node for T {}

pub struct Search<T, IsDone, GetNeighbors>
where
    T: Node,
    IsDone: Fn(&T) -> bool,
    GetNeighbors: Fn(&T) -> Vec<(T, i64)>,
{
    pub start: T,
    pub is_done: IsDone,
    pub get_neighbors: GetNeighbors,
}

impl<T, IsDone, GetNeighbors> Search<T, IsDone, GetNeighbors>
where
    T: Node,
    IsDone: Fn(&T) -> bool,
    GetNeighbors: Fn(&T) -> Vec<(T, i64)>,
{
    pub fn dijkstra(&self) -> Option<i64> {
        let mut queue = DoublePriorityQueue::new();
        queue.push_decrease(self.start.clone(), 0);
        let mut seen = HashSet::new();
        while !queue.is_empty() {
            let (node, weight) = queue.pop_min().unwrap();
            if (self.is_done)(&node) {
                return Some(weight);
            }
            if seen.contains(&node) {
                continue;
            } else {
                seen.insert(node.clone());
            }
            (self.get_neighbors)(&node)
                .into_iter()
                .filter(|(next_node, _)| !seen.contains(next_node))
                .for_each(|(next_node, cost)| {
                    queue.push_decrease(next_node, weight + cost);
                });
        }
        None
    }
}
