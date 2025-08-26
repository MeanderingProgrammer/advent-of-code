const std = @import("std");
const Allocator = std.mem.Allocator;
const Map = std.AutoHashMap;

const aoc = @import("aoc");
const answer = aoc.answer;

pub fn main() !void {
    try answer.timer(solution);
}

fn solution(c: *aoc.Context) !void {
    const line = try aoc.Reader.init(c.allocator()).string();
    const stones = try getStones(c.allocator(), line);
    answer.part1(usize, 185894, try evolve(c.allocator(), stones, 25));
    answer.part2(usize, 221632504974231, try evolve(c.allocator(), stones, 75));
}

fn getStones(allocator: Allocator, line: []const u8) !Map(usize, usize) {
    var stones = Map(usize, usize).init(allocator);
    var it = std.mem.splitScalar(u8, line, ' ');
    while (it.next()) |item| {
        const stone = try aoc.util.decimal(usize, item);
        try increment(&stones, stone, 1);
    }
    return stones;
}

fn evolve(allocator: Allocator, input: Map(usize, usize), blinks: usize) !usize {
    var stones = try input.clone();
    for (0..blinks) |_| {
        var next = Map(usize, usize).init(allocator);
        var it = stones.iterator();
        while (it.next()) |entry| {
            const stone = entry.key_ptr.*;
            const amount = entry.value_ptr.*;
            if (stone == 0) {
                try increment(&next, 1, amount);
            } else {
                const digits = std.math.log10(stone) + 1;
                if (digits % 2 == 1) {
                    try increment(&next, stone * 2024, amount);
                } else {
                    const factor = std.math.pow(usize, 10, digits / 2);
                    try increment(&next, stone / factor, amount);
                    try increment(&next, stone % factor, amount);
                }
            }
        }
        stones.deinit();
        stones = next;
    }
    var result: usize = 0;
    var counts = stones.valueIterator();
    while (counts.next()) |value| {
        result += value.*;
    }
    return result;
}

fn increment(stones: *Map(usize, usize), stone: usize, amount: usize) !void {
    const entry = try stones.getOrPut(stone);
    if (!entry.found_existing) {
        entry.value_ptr.* = 0;
    }
    entry.value_ptr.* += amount;
}
