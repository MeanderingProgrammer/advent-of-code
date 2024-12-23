const aoc = @import("aoc");
const answer = aoc.answer;
const Reader = aoc.reader.Reader;
const Set = aoc.set.Set;
const std = @import("std");
const allocator = std.heap.page_allocator;

const Secret = struct {
    value: usize,
    changes: std.ArrayList(i64),
    sequences: std.AutoHashMap([4]i64, usize),

    fn init(start: usize) Secret {
        return .{
            .value = start,
            .changes = std.ArrayList(i64).init(allocator),
            .sequences = std.AutoHashMap([4]i64, usize).init(allocator),
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
        self.mix_prune(self.value * 64);
        self.mix_prune(self.value / 32);
        self.mix_prune(self.value * 2048);
    }

    fn mix_prune(self: *Secret, value: usize) void {
        self.value ^= value;
        self.value %= 16777216;
    }
};

pub fn main() !void {
    try answer.timer(solution);
}

fn solution() !void {
    const starts = try Reader.init().int_lines();
    const secrets = try get_secrets(starts, 2000);
    answer.part1(usize, 15608699004, part1(secrets));
    answer.part2(usize, 1791, try part2(secrets));
}

fn get_secrets(starts: std.ArrayList(usize), n: usize) !std.ArrayList(Secret) {
    var result = std.ArrayList(Secret).init(allocator);
    for (starts.items) |start| {
        var secret = Secret.init(start);
        try secret.evolve(n);
        try result.append(secret);
    }
    return result;
}

fn part1(secrets: std.ArrayList(Secret)) usize {
    var result: usize = 0;
    for (secrets.items) |secret| {
        result += secret.value;
    }
    return result;
}

fn part2(secrets: std.ArrayList(Secret)) !usize {
    var result: usize = 0;
    const options = try get_options(secrets);
    var it = options.iterator();
    while (it.next()) |sequence| {
        if (sequence[0] + sequence[1] + sequence[2] + sequence[3] > 0) {
            const value = bananas(secrets, sequence.*);
            result = @max(result, value);
        }
    }
    return result;
}

fn get_options(secrets: std.ArrayList(Secret)) !Set([4]i64) {
    var options = Set([4]i64).init(allocator);
    for (secrets.items) |secret| {
        var it = secret.sequences.keyIterator();
        while (it.next()) |sequence| {
            try options.add(sequence.*);
        }
    }
    return options;
}

fn bananas(secrets: std.ArrayList(Secret), sequence: [4]i64) usize {
    var result: usize = 0;
    for (secrets.items) |secret| {
        if (secret.sequences.get(sequence)) |price| {
            result += price;
        }
    }
    return result;
}
