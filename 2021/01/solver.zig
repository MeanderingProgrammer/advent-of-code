const aoc = @import("aoc");
const answer = aoc.answer;
const Reader = aoc.reader.Reader;
const std = @import("std");

pub fn main() !void {
    try answer.timer(solution);
}

fn solution() !void {
    const values = try Reader.init().intLines();
    answer.part1(usize, 1292, windowIncreases(values, 1));
    answer.part2(usize, 1262, windowIncreases(values, 3));
}

fn windowIncreases(values: std.ArrayList(usize), window_size: usize) usize {
    var result: usize = 0;
    for (0..values.items.len - window_size) |i| {
        if (windowSum(values, window_size, i + 1) > windowSum(values, window_size, i)) {
            result += 1;
        }
    }
    return result;
}

fn windowSum(values: std.ArrayList(usize), window_size: usize, start_index: usize) usize {
    var result: usize = 0;
    for (start_index..start_index + window_size) |i| {
        result += values.items[i];
    }
    return result;
}
