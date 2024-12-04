const aoc = @import("aoc");
const answer = aoc.answer;
const Reader = aoc.reader.Reader;
const std = @import("std");

pub fn main() !void {
    try answer.timer(solution);
}

fn solution() !void {
    const values = try Reader.init().read_int();
    answer.part1(usize, 1292, window_increases(values, 1));
    answer.part2(usize, 1262, window_increases(values, 3));
}

fn window_increases(values: std.ArrayList(usize), window_size: usize) usize {
    var result: usize = 0;
    for (0..values.items.len - window_size) |i| {
        if (window_sum(values, window_size, i + 1) > window_sum(values, window_size, i)) {
            result += 1;
        }
    }
    return result;
}

fn window_sum(values: std.ArrayList(usize), window_size: usize, start_index: usize) usize {
    var result: usize = 0;
    for (start_index..start_index + window_size) |i| {
        result += values.items[i];
    }
    return result;
}
