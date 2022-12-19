use std::collections::HashMap;
use snowflake::ProcessUniqueId;

#[derive(Debug, Clone, PartialEq, Eq, Hash)]
struct NodeId {
    id: ProcessUniqueId,
}

impl NodeId {
    fn new() -> Self {
        Self { id: ProcessUniqueId::new() }
    }
}

#[derive(Debug)]
pub struct Graph<T> {
    name_to_id: HashMap<String, NodeId>,
    id_to_node: HashMap<NodeId, T>,
    graph: HashMap<NodeId, Vec<NodeId>>,
}

impl<T> Graph<T> {
    pub fn new() -> Self {
        Self { 
            name_to_id: HashMap::new(),
            id_to_node: HashMap::new(),
            graph: HashMap::new(),
        }
    }

    pub fn get_nodes(&self) -> Vec<&T> {
        self.id_to_node.values().collect()
    }

    pub fn add_node(&mut self, name: String, value: T) {
        if self.name_to_id.contains_key(&name) {
            panic!("Node has already been added");
        }

        let node_id = NodeId::new();
        self.name_to_id.insert(name, node_id.clone());
        self.id_to_node.insert(node_id.clone(), value);
        self.graph.insert(node_id.clone(), Vec::new());
    }

    pub fn add_edge(&mut self, from: &str, to: &str) {
        let from_node = self.get_id(from);
        let to_node = self.get_id(to);

        let existing = self.graph.get_mut(&from_node).unwrap();
        existing.push(to_node);
    }

    pub fn get_node(&self, from: &str) -> &T {
        let node_id = self.get_id(from);
        self.id_to_node.get(&node_id).unwrap()
    }

    pub fn neighbors(&self, from: &str) -> Vec<&T> {
        let node_id = self.get_id(from);
        let neighbors = self.graph.get(&node_id).unwrap();
        neighbors.iter()
            .map(|neighbor| self.id_to_node.get(neighbor).unwrap())
            .collect()
    }

    fn get_id(&self, name: &str) -> NodeId {
        self.name_to_id.get(name).unwrap().clone()
    }
}
