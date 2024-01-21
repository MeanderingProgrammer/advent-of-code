use aoc_lib::answer;
use aoc_lib::reader::Reader;
use id_tree::InsertBehavior;
use id_tree::{Node, NodeId, Tree};

#[derive(Debug)]
struct FileSystem {
    tree: Tree<i64>,
    current: NodeId,
}

impl FileSystem {
    fn new() -> Self {
        let mut tree = Tree::<i64>::new();
        let current = tree.insert(Node::new(0), InsertBehavior::AsRoot).unwrap();
        Self { tree, current }
    }

    fn move_up(&mut self) {
        let current_node = self.tree.get(&self.current).unwrap();
        self.current = current_node.parent().unwrap().clone();
    }

    fn move_down(&mut self) {
        self.current = self.insert(0);
    }

    fn insert_file(&mut self, size: i64) {
        self.insert(size);
    }

    fn insert(&mut self, size: i64) -> NodeId {
        let behavior = InsertBehavior::UnderNode(&self.current);
        self.tree.insert(Node::new(size), behavior).unwrap()
    }

    fn directories(&self) -> Vec<i64> {
        self.tree
            .traverse_pre_order(&self.tree.root_node_id().unwrap())
            .unwrap()
            .filter(|node| !node.children().is_empty())
            .map(|node| self.get_size(node))
            .collect()
    }

    fn get_size(&self, node: &Node<i64>) -> i64 {
        let mut total_size = *node.data();
        for child in node.children() {
            total_size += self.get_size(self.tree.get(child).unwrap());
        }
        total_size
    }
}

fn main() {
    answer::timer(solution);
}

fn solution() {
    // Heavily inspired by https://fasterthanli.me/series/advent-of-code-2022/part-7
    let fs = get_file_system();
    let directories = fs.directories();

    let p1_directories = directories.iter().filter(|&&size| size <= 100_000);
    answer::part1(1141028, p1_directories.sum());

    let size_used = directories.iter().max().unwrap();
    let space_needed = 30_000_000 - (70_000_000 - size_used);
    let p2_directories = directories.iter().filter(|&&size| size >= space_needed);
    answer::part2(8278005, *p2_directories.min().unwrap());
}

fn get_file_system() -> FileSystem {
    let mut fs = FileSystem::new();
    Reader::default().read_lines().iter().for_each(|line| {
        let parts: Vec<&str> = line.split(" ").collect();
        match (parts[0], parts[1]) {
            ("$", "cd") => match parts[2] {
                "/" => {
                    // Do not support going back to root
                }
                ".." => fs.move_up(),
                _ => fs.move_down(),
            },
            ("$", "ls") => {
                // Nothing to do when we see an ls, we just know that the
                // next lines will inform our file system structure
            }
            ("dir", _) => {
                // A directory in a list does nothing, will process it when
                // we change into the directory
            }
            (file_size, _) => fs.insert_file(file_size.parse().unwrap()),
        };
    });
    fs
}
