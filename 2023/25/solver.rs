use aoc_lib::answer;
use aoc_lib::reader::Reader;
use fxhash::FxHashMap;
use rand::seq::{IteratorRandom, SliceRandom};
use rayon::prelude::*;
use std::thread;

#[derive(Debug, Clone, PartialEq, Eq, Hash)]
struct Node<'a> {
    name: &'a str,
    count: usize,
}

impl<'a> Node<'a> {
    fn new(name: &'a str) -> Self {
        Self { name, count: 1 }
    }

    fn combine(&self, other: &Self) -> Self {
        Self {
            name: self.name,
            count: self.count + other.count,
        }
    }
}

#[derive(Debug, Clone)]
struct Graph<'a> {
    graph: FxHashMap<Node<'a>, Vec<Node<'a>>>,
}

impl<'a> Graph<'a> {
    fn new(lines: &'a [String]) -> Self {
        let mut graph = FxHashMap::default();
        lines.iter().for_each(|line| {
            let (node, edges) = line.split_once(": ").unwrap();
            edges.split(' ').for_each(|edge| {
                let node1 = Node::new(node);
                let node2 = Node::new(edge);
                graph
                    .entry(node1.clone())
                    .and_modify(|edges: &mut Vec<Node>| edges.push(node2.clone()))
                    .or_insert(vec![node2.clone()]);
                graph
                    .entry(node2.clone())
                    .and_modify(|edges: &mut Vec<Node>| edges.push(node1.clone()))
                    .or_insert(vec![node1.clone()]);
            });
        });
        Self { graph }
    }

    fn karger(&mut self) {
        let mut rng = rand::thread_rng();
        while self.graph.len() > 2 {
            let n1 = self.graph.keys().choose(&mut rng).unwrap().clone();
            let n2 = self.graph[&n1].choose(&mut rng).unwrap().clone();

            let edges1 = self.get_and_remove(&n1, &n2);
            let edges2 = self.get_and_remove(&n2, &n1);

            let combined = n1.combine(&n2);
            let combined_edges = [edges1.clone(), edges2.clone()].concat();
            self.graph.insert(combined.clone(), combined_edges);

            for edge in &edges1 {
                self.replace(edge, &n1, &combined);
            }
            for edge in &edges2 {
                self.replace(edge, &n2, &combined);
            }
        }
    }

    fn get_and_remove(&mut self, node: &Node<'a>, remove: &Node<'a>) -> Vec<Node<'a>> {
        let mut edges = self.graph.remove(node).unwrap();
        edges.retain(|edge| edge != remove);
        edges
    }

    fn replace(&mut self, neighbor: &Node<'a>, old: &Node<'a>, new: &Node<'a>) {
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
    let graph = Graph::new(&lines);
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
