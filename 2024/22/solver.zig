const std = @import("std");
const Allocator = std.mem.Allocator;
const List = std.array_list.Managed;
const Map = std.AutoHashMap;

const aoc = @import("aoc");
const answer = aoc.answer;

const Secret = struct {
    value: usize,
    changes: List(i64),
    sequences: Map([4]i64, usize),

    fn init(allocator: Allocator, start: usize) Secret {
        return .{
            .value = start,
            .changes = List(i64).init(allocator),
            .sequences = Map([4]i64, usize).init(allocator),
        };
    }

    fn evolve(self: *Secret, n: usize) !void {
        for (0..n) |i| {
            const start: i64 = @intCast(self.value % 10);
            self.step();
            const end: i64 = @intCast(self.value % 10);
            try self.changes.append(end - start);
            if (i >= 3) {
                const sequence = [4]i64{
                    self.changes.items[i - 3],
                    self.changes.items[i - 2],
                    self.changes.items[i - 1],
                    self.changes.items[i],
                };
                if (!self.sequences.contains(sequence)) {
                    try self.sequences.put(sequence, @intCast(end));
                }
            }
        }
    }

    fn step(self: *Secret) void {
        self.mixPrune(self.value * 64);
        self.mixPrune(self.value / 32);
        self.mixPrune(self.value * 2048);
    }

    fn mixPrune(self: *Secret, value: usize) void {
        self.value ^= value;
        self.value %= 16777216;
    }
};

pub fn main() !void {
    try answer.timer(solution);
}

fn solution(c: *aoc.Context) !void {
    const starts = try aoc.Reader.init(c.allocator()).intLines();
    const secrets = try getSecrets(c.allocator(), starts, 2000);
    answer.part1(usize, 15608699004, part1(secrets));
    answer.part2(usize, 1791, try part2(c.allocator(), secrets));
}

fn getSecrets(allocator: Allocator, starts: List(usize), n: usize) !List(Secret) {
    var result = List(Secret).init(allocator);
    for (starts.items) |start| {
        var secret = Secret.init(allocator, start);
        try secret.evolve(n);
        try result.append(secret);
    }
    return result;
}

fn part1(secrets: List(Secret)) usize {
    var result: usize = 0;
    for (secrets.items) |secret| {
        result += secret.value;
    }
    return result;
}

fn part2(allocator: Allocator, secrets: List(Secret)) !usize {
    var result: usize = 0;
    const options = try getOptions(allocator, secrets);
    var it = options.iterator();
    while (it.next()) |sequence| {
        if (sequence[0] + sequence[1] + sequence[2] + sequence[3] > 0) {
            const value = bananas(secrets, sequence.*);
            result = @max(result, value);
        }
    }
    return result;
}

fn getOptions(allocator: Allocator, secrets: List(Secret)) !aoc.Set([4]i64) {
    var options = aoc.Set([4]i64).init(allocator);
    for (secrets.items) |secret| {
        var it = secret.sequences.keyIterator();
        while (it.next()) |sequence| {
            try options.add(sequence.*);
        }
    }
    return options;
}

fn bananas(secrets: List(Secret), sequence: [4]i64) usize {
    var result: usize = 0;
    for (secrets.items) |secret| {
        if (secret.sequences.get(sequence)) |price| {
            result += price;
        }
    }
    return result;
}
