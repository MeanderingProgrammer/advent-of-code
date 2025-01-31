use crate::collections::HashMap;
use std::cmp::Ordering;
use std::collections::BinaryHeap;
use std::hash::Hash;

#[derive(Debug)]
struct Item<I, P> {
    item: I,
    priority: P,
    kind: HeapKind,
}

impl<I, P> Item<I, P> {
    fn new(item: I, priority: P, kind: &HeapKind) -> Self {
        Self {
            item,
            priority,
            kind: kind.clone(),
        }
    }
}

impl<I, P: Ord> PartialEq for Item<I, P> {
    fn eq(&self, other: &Self) -> bool {
        self.priority == other.priority
    }
}

impl<I, P: Ord> Eq for Item<I, P> {}

impl<I, P: Ord> PartialOrd for Item<I, P> {
    fn partial_cmp(&self, other: &Self) -> Option<Ordering> {
        Some(self.cmp(other))
    }
}

impl<I, P: Ord> Ord for Item<I, P> {
    fn cmp(&self, other: &Self) -> Ordering {
        match self.kind {
            HeapKind::Min => other.priority.cmp(&self.priority),
            HeapKind::Max => self.priority.cmp(&other.priority),
        }
    }
}

#[derive(Debug, Clone)]
pub enum HeapKind {
    Max,
    Min,
}

#[derive(Debug)]
pub struct PriorityQueue<I, P> {
    kind: HeapKind,
    heap: BinaryHeap<Item<I, P>>,
    best: HashMap<I, P>,
}

impl<I, P> PriorityQueue<I, P>
where
    I: Clone + Hash + Eq,
    P: Clone + Ord,
{
    pub fn new(kind: HeapKind) -> Self {
        Self {
            kind,
            heap: BinaryHeap::default(),
            best: HashMap::default(),
        }
    }

    pub fn push(&mut self, item: I, priority: P) {
        let better = match self.best.get(&item) {
            None => true,
            Some(current) => match self.kind {
                HeapKind::Min => &priority < current,
                HeapKind::Max => &priority > current,
            },
        };
        if better {
            self.best.insert(item.clone(), priority.clone());
            self.heap.push(Item::new(item, priority, &self.kind));
        }
    }

    pub fn pop(&mut self) -> Option<(I, P)> {
        self.heap.pop().map(|entry| (entry.item, entry.priority))
    }

    pub fn is_empty(&self) -> bool {
        self.heap.is_empty()
    }
}
