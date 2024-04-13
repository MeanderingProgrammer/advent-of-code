use fxhash::FxHashSet;
use std::collections::VecDeque;
use std::fmt::Debug;
use std::hash::Hash;

pub trait Node: Debug + Clone + Hash + Eq {}
impl<T: Debug + Clone + Hash + Eq> Node for T {}

pub struct Search<T, IsDone, GetNeighbors>
where
    T: Node,
    IsDone: Fn(&T) -> bool,
    GetNeighbors: Fn(&T) -> Vec<T>,
{
    pub start: T,
    pub is_done: IsDone,
    pub get_neighbors: GetNeighbors,
}

impl<T, IsDone, GetNeighbors> Search<T, IsDone, GetNeighbors>
where
    T: Node,
    IsDone: Fn(&T) -> bool,
    GetNeighbors: Fn(&T) -> Vec<T>,
{
    pub fn bfs(&self) -> Option<i64> {
        let mut queue = VecDeque::new();
        queue.push_back((self.start.clone(), 0));
        let mut seen = FxHashSet::default();
        while !queue.is_empty() {
            let (node, length) = queue.pop_front().unwrap();
            if (self.is_done)(&node) {
                return Some(length);
            }
            if seen.contains(&node) {
                continue;
            }
            seen.insert(node.clone());
            (self.get_neighbors)(&node)
                .into_iter()
                .filter(|next_node| !seen.contains(next_node))
                .for_each(|next_node| queue.push_back((next_node, length + 1)));
        }
        None
    }
}
