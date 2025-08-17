const std = @import("std");
const aoc = @import("aoc");
const answer = aoc.answer;

pub fn main() !void {
    try answer.timer(solution);
}

fn solution(c: *aoc.Context) !void {
    const data = try aoc.Reader.init(c.allocator()).stringLines();
    std.debug.print("{any}\n", .{data});
    answer.part1(usize, 1, 1);
    answer.part2(usize, 1, 1);
}
