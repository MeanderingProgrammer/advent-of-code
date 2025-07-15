const std = @import("std");
const Allocator = std.mem.Allocator;
const Grid = @import("grid.zig").Grid;
const util = @import("util.zig");

const Strings = std.ArrayList([]const u8);

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

    pub fn ints(self: Reader) !std.ArrayList(usize) {
        const line = try self.string();
        var result = std.ArrayList(usize).init(self.allocator);
        for (line) |ch| {
            try result.append(ch - '0');
        }
        return result;
    }

    pub fn string(self: Reader) ![]const u8 {
        return (try self.stringLines()).items[0];
    }

    pub fn stringLines(self: Reader) !Strings {
        return self.lines([]const u8, identity);
    }

    fn identity(_: Allocator, s: []const u8) ![]const u8 {
        return s;
    }

    pub fn intLines(self: Reader) !std.ArrayList(usize) {
        return self.lines(usize, decimal);
    }

    fn decimal(_: Allocator, s: []const u8) !usize {
        return util.decimal(usize, s);
    }

    pub fn groups(self: Reader) !std.ArrayList(Strings) {
        var result = std.ArrayList(Strings).init(self.allocator);
        for ((try self.read("\n\n")).items) |item| {
            var group = Strings.init(self.allocator);
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

    pub fn lines(self: Reader, comptime T: type, f: fn (Allocator, []const u8) anyerror!T) !std.ArrayList(T) {
        var result = std.ArrayList(T).init(self.allocator);
        for ((try self.read("\n")).items) |line| {
            try result.append(try f(self.allocator, line));
        }
        return result;
    }

    fn read(self: Reader, delimiter: []const u8) !Strings {
        var file = try std.fs.cwd().openFile(self.path, .{});
        defer file.close();

        const buffer = try self.allocator.alloc(u8, try file.getEndPos());
        _ = try file.readAll(buffer);

        var result = Strings.init(self.allocator);
        var it = std.mem.splitSequence(u8, buffer, delimiter);
        while (it.next()) |item| {
            if (item.len > 0) {
                try result.append(item);
            }
        }
        return result;
    }
};
