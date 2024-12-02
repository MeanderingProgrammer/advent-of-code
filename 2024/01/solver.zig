const aoc = @import("aoc");
const std = @import("std");
const allocator = std.heap.page_allocator;

const Pair = struct { usize, usize };

pub fn main() !void {
    try aoc.answer.timer(solution);
}

fn solution() !void {
    const values = try aoc.reader.Reader.init().read(Pair, to_pairs);
    const left = try unzip_sort(values, true);
    const right = try unzip_sort(values, false);
    aoc.answer.part1(3246517, sum_diff(left, right));
    aoc.answer.part2(29379307, similarity(left, right));
}

fn to_pairs(line: []const u8) !Pair {
    var pair = std.mem.tokenizeScalar(u8, line, ' ');
    const first = try std.fmt.parseInt(usize, pair.next() orelse "", 10);
    const second = try std.fmt.parseInt(usize, pair.next() orelse "", 10);
    return Pair{ first, second };
}

fn unzip_sort(values: std.ArrayList(Pair), first: bool) !std.ArrayList(usize) {
    var result = std.ArrayList(usize).init(allocator);
    for (values.items) |value| {
        if (first) {
            try result.append(value[0]);
        } else {
            try result.append(value[1]);
        }
    }
    std.mem.sort(usize, result.items, {}, std.sort.asc(usize));
    return result;
}

fn sum_diff(left: std.ArrayList(usize), right: std.ArrayList(usize)) usize {
    var result: usize = 0;
    for (0..left.items.len) |i| {
        const l = left.items[i];
        const r = right.items[i];
        result += if (l > r) l - r else r - l;
    }
    return result;
}

fn similarity(left: std.ArrayList(usize), right: std.ArrayList(usize)) usize {
    var result: usize = 0;
    for (0..left.items.len) |i| {
        const l = left.items[i];
        result += (l * count(right, l));
    }
    return result;
}

fn count(values: std.ArrayList(usize), value: usize) usize {
    var result: usize = 0;
    for (0..values.items.len) |i| {
        result += if (value == values.items[i]) 1 else 0;
    }
    return result;
}
