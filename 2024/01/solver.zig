const std = @import("std");
const Allocator = std.mem.Allocator;
const aoc = @import("aoc");
const answer = aoc.answer;
const Reader = aoc.reader.Reader;

const Pair = struct { usize, usize };
const Integers = std.ArrayList(usize);

pub fn main() !void {
    try answer.timer(solution);
}

fn solution(allocator: Allocator) !void {
    const values = try Reader.init(allocator).lines(Pair, toPairs);
    const left = try unzipSort(allocator, values, true);
    const right = try unzipSort(allocator, values, false);
    answer.part1(usize, 3246517, sumDiff(left, right));
    answer.part2(usize, 29379307, similarity(left, right));
}

fn toPairs(_: Allocator, line: []const u8) !Pair {
    var pair = std.mem.tokenizeScalar(u8, line, ' ');
    const first = try aoc.util.decimal(usize, pair.next() orelse "");
    const second = try aoc.util.decimal(usize, pair.next() orelse "");
    return .{ first, second };
}

fn unzipSort(allocator: Allocator, values: std.ArrayList(Pair), first: bool) !Integers {
    var result = Integers.init(allocator);
    for (values.items) |value| {
        const item = if (first) value[0] else value[1];
        try result.append(item);
    }
    std.mem.sort(usize, result.items, {}, std.sort.asc(usize));
    return result;
}

fn sumDiff(left: Integers, right: Integers) usize {
    var result: usize = 0;
    for (0..left.items.len) |i| {
        const l = left.items[i];
        const r = right.items[i];
        result += @max(l, r) - @min(l, r);
    }
    return result;
}

fn similarity(left: Integers, right: Integers) usize {
    var result: usize = 0;
    for (0..left.items.len) |i| {
        const l = left.items[i];
        result += (l * count(right, l));
    }
    return result;
}

fn count(values: Integers, target: usize) usize {
    var result: usize = 0;
    for (values.items) |value| {
        result += if (value == target) 1 else 0;
    }
    return result;
}
