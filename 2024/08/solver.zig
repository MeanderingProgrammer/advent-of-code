const aoc = @import("aoc");
const answer = aoc.answer;
const Reader = aoc.reader.Reader;
const std = @import("std");

pub fn main() !void {
    try answer.timer(solution);
}

fn solution() !void {
    const data = try Reader.init().string_lines();
    std.debug.print("{any}\n", .{data});
    answer.part1(usize, 1, 1);
}
