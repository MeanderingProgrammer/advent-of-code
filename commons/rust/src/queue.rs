use fxhash::FxHashMap;
use std::cmp::Ordering;
use std::collections::BinaryHeap;
use std::hash::Hash;

#[derive(Debug)]
struct Item<I, P> {
    item: I,
    priority: P,
    variant: HeapVariant,
}

impl<I, P> Item<I, P> {
    fn new(item: I, priority: P, variant: &HeapVariant) -> Self {
        Self {
            item,
            priority,
            variant: variant.clone(),
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
        match self.variant {
            HeapVariant::Min => other.priority.cmp(&self.priority),
            HeapVariant::Max => self.priority.cmp(&other.priority),
        }
    }
}

#[derive(Debug, Clone)]
pub enum HeapVariant {
    Max,
    Min,
}

#[derive(Debug)]
pub struct PriorityQueue<I, P> {
    variant: HeapVariant,
    heap: BinaryHeap<Item<I, P>>,
    best: FxHashMap<I, P>,
}

impl<I, P> PriorityQueue<I, P>
where
    I: Clone + Hash + Eq,
    P: Clone + Ord,
{
    pub fn new(variant: HeapVariant) -> Self {
        Self {
            variant,
            heap: BinaryHeap::default(),
            best: FxHashMap::default(),
        }
    }

    pub fn push(&mut self, item: I, priority: P) {
        let better = match self.best.get(&item) {
            None => true,
            Some(current) => match self.variant {
                HeapVariant::Min => &priority < current,
                HeapVariant::Max => &priority > current,
            },
        };
        if better {
            self.best.insert(item.clone(), priority.clone());
            self.heap.push(Item::new(item, priority, &self.variant));
        }
    }

    pub fn pop(&mut self) -> Option<(I, P)> {
        self.heap.pop().map(|entry| (entry.item, entry.priority))
    }

    pub fn is_empty(&self) -> bool {
        self.heap.is_empty()
    }
}
