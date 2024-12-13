const std = @import("std");
const Grid = @import("grid.zig").Grid;
const allocator = std.heap.page_allocator;

const Transformers = struct {
    fn identity(line: []const u8) ![]const u8 {
        return line;
    }

    fn to_int(line: []const u8) !usize {
        return std.fmt.parseInt(usize, line, 10);
    }
};

pub const Reader = struct {
    path: []const u8,

    pub fn init() Reader {
        var args = std.process.args();

        const executable = args.next() orelse "";
        var exe_path = std.mem.splitBackwardsScalar(u8, executable, '/');
        var year_date = std.mem.splitScalar(u8, exe_path.first(), '_');
        const year = year_date.next() orelse "";
        const day = year_date.next() orelse "";

        const test_value = args.next() orelse "";
        const file = if (std.mem.eql(u8, test_value, "--test")) "sample.txt" else "data.txt";

        const path = std.mem.join(allocator, "/", &[_][]const u8{ "data", year, day, file }) catch "";
        return .{ .path = path };
    }

    pub fn grid(self: Reader) !Grid {
        return Grid.init(try self.string_lines());
    }

    pub fn ints(self: Reader) !std.ArrayList(usize) {
        const line = try self.string();
        var result = std.ArrayList(usize).init(allocator);
        for (line) |ch| {
            try result.append(ch - '0');
        }
        return result;
    }

    pub fn string(self: Reader) ![]const u8 {
        return (try self.string_lines()).items[0];
    }

    pub fn string_lines(self: Reader) !std.ArrayList([]const u8) {
        return self.lines([]const u8, Transformers.identity);
    }

    pub fn int_lines(self: Reader) !std.ArrayList(usize) {
        return self.lines(usize, Transformers.to_int);
    }

    pub fn groups(self: Reader) !std.ArrayList(std.ArrayList([]const u8)) {
        var result = std.ArrayList(std.ArrayList([]const u8)).init(allocator);
        for ((try self.read("\n\n")).items) |item| {
            var group = std.ArrayList([]const u8).init(allocator);
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

    pub fn lines(self: Reader, comptime T: type, f: fn ([]const u8) anyerror!T) !std.ArrayList(T) {
        var result = std.ArrayList(T).init(allocator);
        for ((try self.read("\n")).items) |line| {
            try result.append(try f(line));
        }
        return result;
    }

    fn read(self: Reader, delimiter: []const u8) !std.ArrayList([]const u8) {
        var file = try std.fs.cwd().openFile(self.path, .{});
        defer file.close();

        const buffer = try allocator.alloc(u8, try file.getEndPos());
        _ = try file.readAll(buffer);

        var result = std.ArrayList([]const u8).init(allocator);
        var it = std.mem.splitSequence(u8, buffer, delimiter);
        while (it.next()) |item| {
            if (item.len > 0) {
                try result.append(item);
            }
        }
        return result;
    }
};
