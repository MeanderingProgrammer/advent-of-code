const std = @import("std");
const Allocator = std.mem.Allocator;
const List = std.array_list.Managed;

const Grid = @import("grid.zig").Grid;
const util = @import("util.zig");

pub const Reader = struct {
    allocator: Allocator,
    path: []const u8,

    pub fn init(allocator: Allocator) Reader {
        var args = std.process.args();

        const executable = args.next() orelse "";
        var exe_path = std.mem.splitBackwardsScalar(u8, executable, '/');
        var year_date = std.mem.splitScalar(u8, exe_path.first(), '_');
        const year = year_date.next() orelse "";
        const day = year_date.next() orelse "";

        const test_value = args.next() orelse "";
        const file = if (std.mem.eql(u8, test_value, "--test")) "sample.txt" else "data.txt";

        const path = std.mem.join(allocator, "/", &[_][]const u8{ "data", year, day, file }) catch "";
        return .{
            .allocator = allocator,
            .path = path,
        };
    }

    pub fn grid(self: Reader) !Grid(u8) {
        var result = Grid(u8).init(self.allocator);
        try result.addLines(try self.stringLines());
        return result;
    }

    pub fn ints(self: Reader) !List(usize) {
        const line = try self.string();
        var result = List(usize).init(self.allocator);
        for (line) |ch| {
            try result.append(ch - '0');
        }
        return result;
    }

    pub fn string(self: Reader) ![]const u8 {
        return (try self.stringLines()).items[0];
    }

    pub fn stringLines(self: Reader) !List([]const u8) {
        return self.lines([]const u8, identity);
    }

    fn identity(_: Allocator, s: []const u8) ![]const u8 {
        return s;
    }

    pub fn intLines(self: Reader) !List(usize) {
        return self.lines(usize, decimal);
    }

    fn decimal(_: Allocator, s: []const u8) !usize {
        return util.decimal(usize, s);
    }

    pub fn groups(self: Reader) !List(List([]const u8)) {
        var result = List(List([]const u8)).init(self.allocator);
        for ((try self.read("\n\n")).items) |item| {
            var group = List([]const u8).init(self.allocator);
            var it = std.mem.splitSequence(u8, item, "\n");
            while (it.next()) |line| {
                if (line.len > 0) {
                    try group.append(line);
                }
            }
            try result.append(group);
        }
        return result;
    }

    pub fn lines(self: Reader, comptime T: type, f: fn (Allocator, []const u8) anyerror!T) !List(T) {
        var result = List(T).init(self.allocator);
        for ((try self.read("\n")).items) |line| {
            try result.append(try f(self.allocator, line));
        }
        return result;
    }

    fn read(self: Reader, delimiter: []const u8) !List([]const u8) {
        var file = try std.fs.cwd().openFile(self.path, .{});
        defer file.close();

        var buffer: [64]u8 = undefined;
        var reader = file.reader(&buffer);
        const input = &reader.interface;
        const text = try input.readAlloc(self.allocator, try file.getEndPos());

        var result = List([]const u8).init(self.allocator);
        var it = std.mem.splitSequence(u8, text, delimiter);
        while (it.next()) |item| {
            if (item.len > 0) {
                try result.append(item);
            }
        }
        return result;
    }
};
