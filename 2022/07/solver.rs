use aoc_lib::answer;
use aoc_lib::reader;
use id_tree::{Node, NodeId, Tree};
use id_tree::InsertBehavior;

#[allow(dead_code)]
#[derive(Debug)]
struct File {
    name: String,
    size: i64,
}

impl File {
    fn new_node(name: String, size: i64) -> Node<Self> {
        Node::new(File {name, size})
    }
}

fn main() {
    // Heavily inspired by https://fasterthanli.me/series/advent-of-code-2022/part-7
    // I have a lot of gaps in my usage of borrows and mutable references, was really helpful!
    
    let tree = create_file_system_tree();

    let directory_sizes: Vec<i64> = tree
        .traverse_pre_order(tree.root_node_id().unwrap()).unwrap()
        .filter(|node| !node.children().is_empty())
        .map(|node| get_size(&tree, node))
        .collect();

    let size_used = directory_sizes.iter().max().unwrap();
    let space_needed = 30_000_000 - (70_000_000 - size_used);

    answer::part1(1141028, directory_sizes.iter().filter(|&&size| size <= 100_000).sum());
    answer::part2(8278005, *directory_sizes.iter().filter(|&&size| size >= space_needed).min().unwrap());
}

fn create_file_system_tree() -> Tree<File> {
    let mut tree = Tree::<File>::new();
    let root = tree
        .insert(
            File::new_node("/".to_string(), 0), 
            InsertBehavior::AsRoot,
        )
        .unwrap();
    let mut current: NodeId = root;

    let lines = reader::read_lines();
    for line in lines {
        let parts: Vec<&str> = line.split(" ").collect();
        match (parts[0], parts[1]) {
            ("$", "cd") => match parts[2] {
                "/" => {
                    // Do not support going back to root currently
                },
                ".." => {
                    current = tree.get(&current).unwrap().parent().unwrap().clone();
                },
                path => {
                    current = tree
                        .insert(
                            File::new_node(path.to_string(), 0), 
                            InsertBehavior::UnderNode(&current),
                        )
                        .unwrap();
                },
            },
            ("$", "ls") => {
                // Nothing to do when we see an ls, we just know that he next lines 
                // will inform our tree structure contents
            },
            ("dir", _) => {
                // A directory in a list does nothing, will process it when we change
                // into the directory
            },
            (file_size, file_name) => {
                tree
                    .insert(
                        File::new_node(file_name.to_string(), file_size.parse::<i64>().unwrap()), 
                        InsertBehavior::UnderNode(&current),
                    )
                    .unwrap();
            },
        };
    }

    tree
}

fn get_size(tree: &Tree<File>, node: &Node<File>) -> i64 {
    let mut total_size = node.data().size;
    for child in node.children() {
        total_size += get_size(tree, tree.get(child).unwrap());
    }
    total_size
}
