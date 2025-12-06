const std = @import("std");
const List = std.array_list.Managed;

const Point = @import("point.zig").Point;

pub fn Grid(comptime T: type) type {
    const Map = std.AutoHashMap(Point, T);

    return struct {
        allocator: std.mem.Allocator,
        grid: Map,

        const Self = @This();

        pub fn init(allocator: std.mem.Allocator) Self {
            return .{
                .allocator = allocator,
                .grid = Map.init(allocator),
            };
        }

        pub fn contains(self: Self, point: Point) bool {
            return self.grid.contains(point);
        }

        pub fn get(self: Self, point: Point) ?T {
            return self.grid.get(point);
        }

        pub fn put(self: *Self, point: Point, value: T) !void {
            try self.grid.put(point, value);
        }

        pub fn addLines(self: *Self, lines: List([]const T)) !void {
            for (lines.items, 0..) |line, y| {
                for (line, 0..) |value, x| {
                    const point = Point.init(@intCast(x), @intCast(y));
                    try self.put(point, value);
                }
            }
        }

        pub fn points(self: Self) Map.KeyIterator {
            return self.grid.keyIterator();
        }

        pub fn iterator(self: *const Self) Map.Iterator {
            return self.grid.iterator();
        }

        pub fn getValues(self: *const Self, value: T) !List(Point) {
            var result = List(Point).init(self.allocator);
            var it = self.iterator();
            while (it.next()) |entry| {
                if (entry.value_ptr.* == value) {
                    try result.append(entry.key_ptr.*);
                }
            }
            return result;
        }

        pub fn string(self: Self) ![]const u8 {
            var bound = Point.init(0, 0);
            var it = self.points();
            while (it.next()) |point| {
                bound.x = @max(bound.x, point.x);
                bound.y = @max(bound.y, point.y);
            }

            var result = List(u8).init(self.allocator);
            var y: i64 = 0;
            while (y <= bound.y) : (y += 1) {
                var x: i64 = 0;
                while (x <= bound.x) : (x += 1) {
                    if (self.get(Point.init(x, y))) |value| {
                        try std.fmt.format(result.writer(), "{any}", .{value});
                    } else {
                        try result.append('.');
                    }
                }
                try result.append('\n');
            }
            return result.items;
        }
    };
}
