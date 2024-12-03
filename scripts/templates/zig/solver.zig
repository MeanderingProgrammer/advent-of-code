const aoc = @import("aoc");
const std = @import("std");

pub fn main() !void {
    try aoc.answer.timer(solution);
}

fn solution() !void {
    const data = try aoc.reader.Reader.init().read_lines();
    std.debug.print("{any}", .{data});
    aoc.answer.part1(usize, 1, 1);
}
