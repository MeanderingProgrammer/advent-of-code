const std = @import("std");
const Allocator = std.mem.Allocator;
const aoc = @import("aoc");
const answer = aoc.answer;
const Reader = aoc.reader.Reader;

pub fn main() !void {
    try answer.timer(solution);
}

fn solution(allocator: Allocator) !void {
    const data = try Reader.init(allocator).stringLines();
    std.debug.print("{any}\n", .{data});
    answer.part1(usize, 1, 1);
    answer.part2(usize, 1, 1);
}
