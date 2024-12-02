const std = @import("std");
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
        const test_value = args.next() orelse "";

        var exe_path = std.mem.splitBackwards(u8, executable, "/");
        var year_date = std.mem.splitScalar(u8, exe_path.first(), '_');
        const year = year_date.next() orelse "";
        const day = year_date.next() orelse "";

        var parts = std.ArrayList([]const u8).init(allocator);
        parts.append("data") catch {};
        parts.append(year) catch {};
        parts.append(day) catch {};
        if (std.mem.eql(u8, test_value, "--test")) {
            parts.append("sample.txt") catch {};
        } else {
            parts.append("data.txt") catch {};
        }

        const path = std.mem.join(allocator, "/", parts.items) catch "";
        return Reader{ .path = path };
    }

    pub fn read_lines(self: Reader) !std.ArrayList([]const u8) {
        return self.read([]const u8, Transformers.identity);
    }

    pub fn read_int(self: Reader) !std.ArrayList(usize) {
        return self.read(usize, Transformers.to_int);
    }

    pub fn read(self: Reader, comptime T: type, f: fn ([]const u8) anyerror!T) !std.ArrayList(T) {
        var file = try std.fs.cwd().openFile(self.path, .{});
        defer file.close();

        const buffer = try allocator.alloc(u8, try file.getEndPos());
        _ = try file.readAll(buffer);
        var it = std.mem.splitScalar(u8, buffer, '\n');

        var result = std.ArrayList(T).init(allocator);
        while (it.next()) |line| {
            if (line.len > 0) {
                try result.append(try f(line));
            }
        }
        return result;
    }
};
