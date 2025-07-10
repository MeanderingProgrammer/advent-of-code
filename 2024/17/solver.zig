const aoc = @import("aoc");
const answer = aoc.answer;
const Reader = aoc.reader.Reader;
const std = @import("std");
const Allocator = std.mem.Allocator;

const Computer = struct {
    a: usize,
    b: usize,
    c: usize,
    memory: std.ArrayList(usize),
    ip: usize,
    out: std.ArrayList(usize),

    fn init(allocator: Allocator, a: usize, memory: std.ArrayList(usize)) !Computer {
        return .{
            .a = a,
            .b = 0,
            .c = 0,
            .memory = memory,
            .ip = 0,
            .out = std.ArrayList(usize).init(allocator),
        };
    }

    pub fn reset(self: *Computer, a: usize) void {
        self.a = a;
        self.b = 0;
        self.c = 0;
        self.ip = 0;
        self.out.clearRetainingCapacity();
    }

    fn run(self: *Computer) !void {
        while (self.ip + 1 < self.memory.items.len) {
            const opcode = self.memory.items[self.ip];
            const operand = self.memory.items[self.ip + 1];
            if (!(try self.operation(opcode, operand))) {
                self.ip += 2;
            }
        }
    }

    fn operation(self: *Computer, opcode: usize, operand: usize) !bool {
        var jumped = false;
        if (opcode == 0) {
            self.a = self.a / std.math.pow(usize, 2, try self.combo(operand));
        } else if (opcode == 1) {
            self.b = self.b ^ operand;
        } else if (opcode == 2) {
            self.b = (try self.combo(operand)) % 8;
        } else if (opcode == 3) {
            if (self.a != 0) {
                self.ip = operand;
                jumped = true;
            }
        } else if (opcode == 4) {
            self.b = self.b ^ self.c;
        } else if (opcode == 5) {
            const out = (try self.combo(operand)) % 8;
            try self.out.append(out);
        } else if (opcode == 6) {
            self.b = self.a / std.math.pow(usize, 2, try self.combo(operand));
        } else if (opcode == 7) {
            self.c = self.a / std.math.pow(usize, 2, try self.combo(operand));
        } else {
            return error.UnknownOpcode;
        }
        return jumped;
    }

    fn combo(self: *Computer, operand: usize) !usize {
        if (operand >= 0 and operand <= 3) {
            return operand;
        } else if (operand == 4) {
            return self.a;
        } else if (operand == 5) {
            return self.b;
        } else if (operand == 6) {
            return self.c;
        } else {
            return error.UnknownCombo;
        }
    }
};

pub fn main() !void {
    try answer.timer(solution);
}

fn solution(allocator: Allocator) !void {
    const groups = try Reader.init(allocator).groups();
    const a = try parseRegister(groups.items[0]);
    const memory = try parseMemory(allocator, groups.items[1]);
    var computer = try Computer.init(allocator, a, memory);
    answer.part1([]const u8, "7,0,3,1,2,6,3,7,1", try part1(allocator, &computer));
    answer.part2(usize, 109020013201563, try part2(allocator, &computer));
}

fn parseRegister(lines: std.ArrayList([]const u8)) !usize {
    // Register A: 729
    var it = std.mem.splitBackwardsScalar(u8, lines.items[0], ' ');
    return try std.fmt.parseInt(usize, it.first(), 10);
}

fn parseMemory(allocator: Allocator, lines: std.ArrayList([]const u8)) !std.ArrayList(usize) {
    // Program: 0,1,5,4,3,0
    var it = std.mem.splitBackwardsScalar(u8, lines.items[0], ' ');
    var result = std.ArrayList(usize).init(allocator);
    var command_it = std.mem.splitScalar(u8, it.first(), ',');
    while (command_it.next()) |ch| {
        try result.append(try std.fmt.parseInt(usize, ch, 10));
    }
    return result;
}

fn part1(allocator: Allocator, computer: *Computer) ![]const u8 {
    try computer.run();
    var values = std.ArrayList([]const u8).init(allocator);
    for (computer.out.items) |value| {
        try values.append(try std.fmt.allocPrint(allocator, "{}", .{value}));
    }
    return try std.mem.join(allocator, ",", values.items);
}

fn part2(allocator: Allocator, computer: *Computer) !usize {
    return (try recursiveBacktracking(allocator, computer, 0, 0)).?;
}

fn recursiveBacktracking(allocator: Allocator, computer: *Computer, a: usize, i: usize) !?usize {
    // There are 4 key aspects of the input program:
    //  1) 5,5 -> out.add(b % 8)        add bottom 3 bits of "b" to the output
    //  2) 2,4 -> b = a % 8             bottom 3 bits of "b" are determined by bottom 3 bits
    //                                  of "a" + some math on the other bits of "a" not shown
    //  3) 0,3 -> a = a / 8             on each iteration bottom 3 bits of "a" are removed
    //  4) 3,0 -> if (a != 0): ip = 0   loop program until "a" == 0
    //
    // Putting this altogether it means that the last value in the output depends only on
    // the top 3 bits of "a", the second to last value depends depends on the top 6 bits,
    // and so on. This means we can fix the top bits based on them working for the last
    // values of the output and gradually build up the solution. When solving for some
    // output index we need to consider all options for the bottom 3 bits that generate a
    // valid output. Since we consider options from low to hi the first option that
    // matches at all indices will also be the lowest valid value for "a".
    const program = computer.memory.items;
    if (program.len == i) {
        return a;
    }
    const out = program[program.len - 1 - i];
    const options = try getOptions(allocator, computer, out, a * 8);
    for (options.items) |option| {
        const result = try recursiveBacktracking(allocator, computer, a * 8 + option, i + 1);
        if (result != null) {
            return result;
        }
    }
    return null;
}

fn getOptions(allocator: Allocator, computer: *Computer, out: usize, a: usize) !std.ArrayList(usize) {
    var result = std.ArrayList(usize).init(allocator);
    for (0..8) |i| {
        computer.reset(a + i);
        try computer.run();
        if (computer.out.items[0] == out) {
            try result.append(i);
        }
    }
    return result;
}
