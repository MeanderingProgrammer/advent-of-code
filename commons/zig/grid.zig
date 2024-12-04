const std = @import("std");
const Point = @import("point.zig").Point;
const allocator = std.heap.page_allocator;

pub const Grid = struct {
    grid: std.AutoHashMap(Point, u8),

    pub fn init(lines: std.ArrayList([]const u8)) !Grid {
        var grid = std.AutoHashMap(Point, u8).init(allocator);
        for (lines.items, 0..) |line, y| {
            for (line, 0..) |value, x| {
                try grid.put(Point.init(@intCast(x), @intCast(y)), value);
            }
        }
        return Grid{ .grid = grid };
    }

    pub fn get(self: Grid, point: Point) ?u8 {
        return self.grid.get(point);
    }

    pub fn points(self: Grid) !std.ArrayList(Point) {
        var result = std.ArrayList(Point).init(allocator);
        var it = self.grid.iterator();
        while (it.next()) |entry| {
            try result.append(entry.key_ptr.*);
        }
        return result;
    }
};
