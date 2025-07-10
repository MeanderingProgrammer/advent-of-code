const std = @import("std");
const Allocator = std.mem.Allocator;

pub fn PriorityQueue(comptime T: type) type {
    const Node = struct {
        value: T,
        cost: usize,
    };
    const List = std.ArrayList(Node);
    return struct {
        list: List,

        const Self = @This();

        pub fn init(allocator: Allocator) Self {
            return .{ .list = List.init(allocator) };
        }

        pub fn push(self: *Self, value: T, cost: usize) !void {
            const node = Node{ .value = value, .cost = cost };
            try self.list.insert(self.getIndex(cost), node);
        }

        fn getIndex(self: *Self, cost: usize) usize {
            var lo: usize = 0;
            var hi: usize = self.list.items.len;
            while (lo < hi) {
                const mid = (lo + hi) / 2;
                const value = self.list.items[mid].cost;
                if (value < cost) {
                    hi = mid;
                } else {
                    lo = mid + 1;
                }
            }
            return lo;
        }

        pub fn pop(self: *Self) Node {
            return self.list.pop().?;
        }

        pub fn isEmpty(self: Self) bool {
            return self.list.items.len == 0;
        }
    };
}
