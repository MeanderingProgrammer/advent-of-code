use aoc_lib::answer;
use aoc_lib::reader::Reader;
use fxhash::FxHashMap;
use rand::seq::{IteratorRandom, SliceRandom};
use rayon::prelude::*;
use std::thread;

#[derive(Debug, Clone, PartialEq, Eq, Hash)]
struct Node {
    id: usize,
    count: usize,
}

impl Node {
    fn new(id: usize) -> Self {
        Self { id, count: 1 }
    }

    fn combine(&self, other: &Self) -> Self {
        Self {
            id: self.id,
            count: self.count + other.count,
        }
    }
}

#[derive(Debug, Clone)]
struct Graph {
    graph: FxHashMap<Node, Vec<Node>>,
}

impl Graph {
    fn new(lines: Vec<String>) -> Self {
        let data: FxHashMap<&str, Vec<&str>> = lines
            .iter()
            .map(|line| {
                let (node, edges) = line.split_once(": ").unwrap();
                (node, edges.split(' ').collect())
            })
            .collect();

        let mut ids: FxHashMap<&str, usize> = FxHashMap::default();
        data.iter().for_each(|(node, edges)| {
            Self::add_node(&mut ids, node);
            edges.iter().for_each(|edge| {
                Self::add_node(&mut ids, edge);
            });
        });

        let mut graph: FxHashMap<Node, Vec<Node>> = FxHashMap::default();
        data.iter().for_each(|(node, edges)| {
            edges.iter().for_each(|edge| {
                let (n1, n2) = (Node::new(ids[node]), Node::new(ids[edge]));
                graph.entry(n1.clone()).or_default().push(n2.clone());
                graph.entry(n2.clone()).or_default().push(n1.clone());
            });
        });

        Self { graph }
    }

    fn add_node<'a>(ids: &mut FxHashMap<&'a str, usize>, node: &'a str) {
        if !ids.contains_key(node) {
            ids.insert(node, ids.len());
        }
    }

    fn karger(&mut self) {
        let mut rng = rand::thread_rng();
        while self.graph.len() > 2 {
            let n1 = self.graph.keys().choose(&mut rng).unwrap().clone();
            let n2 = self.graph[&n1].choose(&mut rng).unwrap().clone();

            let edges1 = self.get_and_remove(&n1, &n2);
            let edges2 = self.get_and_remove(&n2, &n1);

            let combined = n1.combine(&n2);
            for edge in &edges1 {
                self.replace(edge, &n1, &combined);
            }
            for edge in &edges2 {
                self.replace(edge, &n2, &combined);
            }
            self.graph.insert(combined, [edges1, edges2].concat());
        }
    }

    fn get_and_remove(&mut self, node: &Node, remove: &Node) -> Vec<Node> {
        let mut edges = self.graph.remove(node).unwrap();
        edges.retain(|edge| edge != remove);
        edges
    }

    fn replace(&mut self, neighbor: &Node, old: &Node, new: &Node) {
        self.graph
            .get_mut(neighbor)
            .unwrap()
            .iter_mut()
            .for_each(|edge| {
                if edge == old {
                    *edge = new.clone();
                }
            });
    }

    fn cut_size(&self) -> usize {
        self.graph.values().next().unwrap().len()
    }

    fn value(&self) -> usize {
        self.graph.keys().map(|node| node.count).product()
    }
}

fn main() {
    answer::timer(solution);
}

fn solution() {
    let lines = Reader::default().read_lines();
    let graph = Graph::new(lines);
    answer::part1(567606, until_cut_size(graph, 3));
}

fn until_cut_size(graph: Graph, size: usize) -> usize {
    let threads = thread::available_parallelism().unwrap().get();
    loop {
        let found_value = (0..threads).into_par_iter().find_map_any(|_| {
            let mut graph_copy = graph.clone();
            graph_copy.karger();
            if graph_copy.cut_size() == size {
                Some(graph_copy.value())
            } else {
                None
            }
        });
        if let Some(value) = found_value {
            return value;
        }
    }
}
