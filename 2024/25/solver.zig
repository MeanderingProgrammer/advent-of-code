const std = @import("std");
const aoc = @import("aoc");
const answer = aoc.answer;

const Strings = std.ArrayList([]const u8);

const Version = enum {
    Lock,
    Key,

    fn init(lines: Strings) !Version {
        if (all(lines, 5, 0)) {
            return Version.Lock;
        } else if (all(lines, 5, 6)) {
            return Version.Key;
        } else {
            return error.InvalidVersion;
        }
    }

    fn all(lines: Strings, width: usize, y: usize) bool {
        for (0..width) |x| {
            if (lines.items[y][x] != '#') {
                return false;
            }
        }
        return true;
    }
};

const Schematic = struct {
    version: Version,
    values: [5]usize,

    fn init(lines: Strings) !Schematic {
        const version = try Version.init(lines);
        var values = [5]usize{ 0, 0, 0, 0, 0 };
        for (0..5) |x| {
            values[x] = gap(lines, x).?;
        }
        return .{
            .version = version,
            .values = values,
        };
    }

    fn gap(lines: Strings, x: usize) ?usize {
        for (1..7) |y| {
            if (lines.items[y - 1][x] != lines.items[y][x]) {
                return y;
            }
        }
        return null;
    }
};

pub fn main() !void {
    try answer.timer(solution);
}

fn solution(c: *aoc.Context) !void {
    const groups = try aoc.Reader.init(c.allocator()).groups();
    answer.part1(usize, 3439, try solve(c.allocator(), groups));
}

fn solve(allocator: std.mem.Allocator, groups: std.ArrayList(Strings)) !usize {
    var keys = std.ArrayList([5]usize).init(allocator);
    var locks = std.ArrayList([5]usize).init(allocator);
    for (groups.items) |lines| {
        const schematic = try Schematic.init(lines);
        switch (schematic.version) {
            Version.Key => try keys.append(schematic.values),
            Version.Lock => try locks.append(schematic.values),
        }
    }

    var result: usize = 0;
    for (locks.items) |lock| {
        for (keys.items) |key| {
            const does_fit = fits(lock, key);
            result += if (does_fit) 1 else 0;
        }
    }
    return result;
}

fn fits(lock: [5]usize, key: [5]usize) bool {
    for (0..5) |x| {
        if (lock[x] > key[x]) {
            return false;
        }
    }
    return true;
}
