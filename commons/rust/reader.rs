use std::fs::File;
use std::io::{BufRead, BufReader};


pub fn read() {
    let file = File::open("data.txt").expect("no such file");
    let reader = BufReader::new(file);

    for line in reader.lines() {
        println!("{}", line.expect("no such file"));
    }
}
