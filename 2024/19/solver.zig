const aoc = @import("aoc");
const answer = aoc.answer;
const Reader = aoc.reader.Reader;
const std = @import("std");
const allocator = std.heap.page_allocator;

const Patterns = struct {
    towels: std.ArrayList([]const u8),
    cache: std.StringHashMap(usize),

    fn init(lines: std.ArrayList([]const u8)) !Patterns {
        var towels = std.ArrayList([]const u8).init(allocator);
        var it = std.mem.splitSequence(u8, lines.items[0], ", ");
        while (it.next()) |towel| {
            try towels.append(towel);
        }
        return .{ .towels = towels, .cache = std.StringHashMap(usize).init(allocator) };
    }

    fn ways(self: *Patterns, target: []const u8) !usize {
        if (target.len == 0) {
            return 1;
        }
        if (self.cache.get(target)) |result| {
            return result;
        }
        var result: usize = 0;
        for (self.towels.items) |towel| {
            if (std.mem.eql(u8, towel, target[0..towel.len])) {
                const rest = target[towel.len..];
                result += try self.ways(rest);
            }
        }
        try self.cache.put(target, result);
        return result;
    }
};

pub fn main() !void {
    try answer.timer(solution);
}

fn solution() !void {
    const groups = try Reader.init().groups();
    var patterns = try Patterns.init(groups.items[0]);
    const targets = groups.items[1];
    answer.part1(usize, 367, try possible(&patterns, targets));
    answer.part2(usize, 724388733465031, try arrangements(&patterns, targets));
}

fn possible(patterns: *Patterns, targets: std.ArrayList([]const u8)) !usize {
    var result: usize = 0;
    for (targets.items) |target| {
        result += if (try patterns.ways(target) > 0) 1 else 0;
    }
    return result;
}

fn arrangements(patterns: *Patterns, targets: std.ArrayList([]const u8)) !usize {
    var result: usize = 0;
    for (targets.items) |target| {
        result += try patterns.ways(target);
    }
    return result;
}
