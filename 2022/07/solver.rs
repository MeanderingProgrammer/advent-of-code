use aoc::prelude::*;

#[derive(Debug, Default)]
struct Node {
    size: usize,
    parent: Option<usize>,
    children: Vec<usize>,
}

impl Node {
    fn new(size: usize, parent: usize) -> Self {
        Self {
            size,
            parent: Some(parent),
            children: Vec::default(),
        }
    }

    fn add(&mut self, child: usize) {
        self.children.push(child);
    }

    fn directory(&self) -> bool {
        !self.children.is_empty()
    }
}

#[derive(Debug)]
struct FileSystem {
    id: usize,
    tree: HashMap<usize, Node>,
}

impl Default for FileSystem {
    fn default() -> Self {
        let mut tree = HashMap::default();
        tree.insert(0, Node::default());
        Self { id: 0, tree }
    }
}

impl FileSystem {
    fn up(&mut self) {
        self.id = self.tree[&self.id].parent.unwrap();
    }

    fn down(&mut self) {
        self.id = self.insert(0);
    }

    fn file(&mut self, size: usize) {
        self.insert(size);
    }

    fn insert(&mut self, size: usize) -> usize {
        let id = self.tree.len();
        self.tree.get_mut(&self.id).unwrap().add(id);
        self.tree.insert(id, Node::new(size, self.id));
        id
    }

    fn directories(&self) -> impl Iterator<Item = usize> + '_ {
        self.tree
            .values()
            .filter(|node| node.directory())
            .map(|node| self.get_size(node))
    }

    fn get_size(&self, node: &Node) -> usize {
        let size: usize = node
            .children
            .iter()
            .map(|child| self.get_size(&self.tree[child]))
            .sum();
        node.size + size
    }
}

fn main() {
    answer::timer(solution);
}

fn solution() {
    // Originally inspired by https://fasterthanli.me/series/advent-of-code-2022/part-7
    let lines = Reader::default().lines();
    let fs = get_file_system(&lines);

    let part1 = fs.directories().filter(|size| *size <= 100_000).sum();
    answer::part1(1141028, part1);

    let size_used = fs.directories().max().unwrap();
    let space_needed = 30_000_000 - (70_000_000 - size_used);
    let part2 = fs.directories().filter(|size| *size >= space_needed).min();
    answer::part2(8278005, part2.unwrap());
}

fn get_file_system(lines: &[String]) -> FileSystem {
    let mut fs = FileSystem::default();
    lines.iter().for_each(|line| {
        let parts: Vec<&str> = line.split(' ').collect();
        match (parts[0], parts[1]) {
            ("$", "cd") => match parts[2] {
                "/" => {
                    // No support for going to root, happens on first line
                }
                ".." => fs.up(),
                _ => fs.down(),
            },
            ("$", "ls") => {
                // Nothing to do when we see an ls, we just know that the
                // next lines will inform our file system structure
            }
            ("dir", _) => {
                // A directory in a list does nothing, will process it when
                // we change into the directory
            }
            (size, _) => fs.file(size.parse().unwrap()),
        };
    });
    fs
}
