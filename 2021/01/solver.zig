const std = @import("std");
const List = std.array_list.Managed;

const aoc = @import("aoc");
const answer = aoc.answer;

pub fn main() !void {
    try answer.timer(solution);
}

fn solution(c: *aoc.Context) !void {
    const values = try aoc.Reader.init(c.allocator()).intLines();
    answer.part1(usize, 1292, increases(values, 1));
    answer.part2(usize, 1262, increases(values, 3));
}

fn increases(values: List(usize), n: usize) usize {
    var result: usize = 0;
    for (0..values.items.len - n) |i| {
        if (sum(values, n, i + 1) > sum(values, n, i)) {
            result += 1;
        }
    }
    return result;
}

fn sum(values: List(usize), n: usize, start: usize) usize {
    var result: usize = 0;
    for (start..start + n) |i| {
        result += values.items[i];
    }
    return result;
}
