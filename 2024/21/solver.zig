const std = @import("std");
const aoc = @import("aoc");
const answer = aoc.answer;
const Counts = std.AutoHashMap(Section, usize);
const Sections = std.ArrayList(Section);

const Section = struct {
    start: u8,
    end: u8,
};

const Keypad = struct {
    allocator: std.mem.Allocator,
    grid: std.AutoHashMap(u8, aoc.Point),
    home: aoc.Point,
    illegal: aoc.Point,
    cache: std.AutoHashMap(Section, Sections),

    fn init(allocator: std.mem.Allocator, numeric: bool) !Keypad {
        var grid = std.AutoHashMap(u8, aoc.Point).init(allocator);
        if (numeric) {
            // | 7 | 8 | 9 |
            try grid.put('7', aoc.Point.init(0, 0));
            try grid.put('8', aoc.Point.init(1, 0));
            try grid.put('9', aoc.Point.init(2, 0));
            // | 4 | 5 | 6 |
            try grid.put('4', aoc.Point.init(0, 1));
            try grid.put('5', aoc.Point.init(1, 1));
            try grid.put('6', aoc.Point.init(2, 1));
            // | 1 | 2 | 3 |
            try grid.put('1', aoc.Point.init(0, 2));
            try grid.put('2', aoc.Point.init(1, 2));
            try grid.put('3', aoc.Point.init(2, 2));
            // |   | 0 | A |
            try grid.put('0', aoc.Point.init(1, 3));
            try grid.put('A', aoc.Point.init(2, 3));
        } else {
            // |   | ^ | A |
            try grid.put('^', aoc.Point.init(1, 0));
            try grid.put('A', aoc.Point.init(2, 0));
            // | < | v | > |
            try grid.put('<', aoc.Point.init(0, 1));
            try grid.put('v', aoc.Point.init(1, 1));
            try grid.put('>', aoc.Point.init(2, 1));
        }
        const home = grid.get('A').?;
        return .{
            .allocator = allocator,
            .grid = grid,
            .home = home,
            .illegal = aoc.Point.init(0, home.y),
            .cache = std.AutoHashMap(Section, Sections).init(allocator),
        };
    }

    fn run(self: *Keypad, sections: Counts) !Counts {
        var result = Counts.init(self.allocator);
        var it = sections.iterator();
        while (it.next()) |entry| {
            const section = entry.key_ptr.*;
            const count = entry.value_ptr.*;
            const cache = try self.cache.getOrPut(section);
            if (!cache.found_existing) {
                cache.value_ptr.* = try self.compute(section);
            }
            for (cache.value_ptr.items) |value| {
                const out = try result.getOrPut(value);
                if (!out.found_existing) {
                    out.value_ptr.* = 0;
                }
                out.value_ptr.* += count;
            }
        }
        return result;
    }

    fn compute(self: *Keypad, section: Section) !Sections {
        const start = self.grid.get(section.start).?;
        const end = self.grid.get(section.end).?;

        // Moving vertically first is illegal since we would enter illegal corner
        const vertical = aoc.Point.init(start.x, end.y);
        // Moving horizontally first is illegal since we would enter illegal corner
        const horizontal = aoc.Point.init(end.x, start.y);

        const dx = end.x - start.x;
        const dy = end.y - start.y;

        var result = Sections.init(self.allocator);
        var previous: u8 = 'A';
        if ((dx > 0 and !self.illegal.eql(vertical)) or self.illegal.eql(horizontal)) {
            previous = try append(&result, previous, dy, true);
            previous = try append(&result, previous, dx, false);
        } else {
            previous = try append(&result, previous, dx, false);
            previous = try append(&result, previous, dy, true);
        }
        try result.append(Section{ .start = previous, .end = 'A' });
        return result;
    }

    fn append(result: *Sections, start: u8, delta: i64, vertical: bool) !u8 {
        const x: u8 = if (delta < 0) '<' else '>';
        const y: u8 = if (delta < 0) '^' else 'v';
        const value: u8 = if (vertical) y else x;
        var previous = start;
        for (0..@abs(delta)) |_| {
            try result.append(Section{ .start = previous, .end = value });
            previous = value;
        }
        return previous;
    }
};

const Layers = struct {
    allocator: std.mem.Allocator,
    numeric: Keypad,
    direction: Keypad,
    size: usize,

    fn init(allocator: std.mem.Allocator, size: usize) !Layers {
        return .{
            .allocator = allocator,
            .numeric = try Keypad.init(allocator, true),
            .direction = try Keypad.init(allocator, false),
            .size = size,
        };
    }

    fn complexity(self: *Layers, sequence: []const u8) !usize {
        var result = try self.convert(sequence);
        result = try self.numeric.run(result);
        for (0..self.size) |_| {
            result = try self.direction.run(result);
        }
        const length = len(result);

        const numeric = sequence[0 .. sequence.len - 1];
        const value = try aoc.util.decimal(usize, numeric);

        return length * value;
    }

    fn convert(self: *Layers, sequence: []const u8) !Counts {
        var result = Counts.init(self.allocator);
        var start: u8 = 'A';
        for (sequence) |end| {
            const section = Section{ .start = start, .end = end };
            try result.put(section, 1);
            start = end;
        }
        return result;
    }

    fn len(sections: Counts) usize {
        var result: usize = 0;
        var it = sections.iterator();
        while (it.next()) |section| {
            result += section.value_ptr.*;
        }
        return result;
    }
};

pub fn main() !void {
    try answer.timer(solution);
}

fn solution(c: *aoc.Context) !void {
    const sequences = try aoc.Reader.init(c.allocator()).stringLines();
    answer.part1(usize, 155252, try solve(c.allocator(), sequences, 2));
    answer.part2(usize, 195664513288128, try solve(c.allocator(), sequences, 25));
}

fn solve(allocator: std.mem.Allocator, sequences: std.ArrayList([]const u8), size: usize) !usize {
    var layers = try Layers.init(allocator, size);
    var result: usize = 0;
    for (sequences.items) |sequence| {
        result += try layers.complexity(sequence);
    }
    return result;
}
