const aoc = @import("aoc");
const answer = aoc.answer;
const Reader = aoc.reader.Reader;
const Set = aoc.set.Set;
const std = @import("std");
const Allocator = std.mem.Allocator;

const Pages = std.ArrayList(usize);
const Rules = std.AutoHashMap(usize, Pages);
const Orders = std.ArrayList(Order);
const Order = struct {
    allocator: Allocator,
    pages: Pages,

    fn init(allocator: Allocator, line: []const u8) !Order {
        var pages = Pages.init(allocator);
        var it = std.mem.splitScalar(u8, line, ',');
        while (it.next()) |page| {
            try pages.append(try toInt(page));
        }
        return .{ .allocator = allocator, .pages = pages };
    }

    fn middle(self: Order) usize {
        return self.pages.items[self.pages.items.len / 2];
    }

    fn valid(self: Order, rules: Rules) !bool {
        var seen = Set(usize).init(self.allocator);
        for (self.pages.items) |page| {
            try seen.add(page);
            if (rules.get(page)) |illegal| {
                for (illegal.items) |p| {
                    if (seen.contains(p)) {
                        return false;
                    }
                }
            }
        }
        return true;
    }

    fn fix(self: *Order, deps: Rules) !Order {
        var pages = Pages.init(self.allocator);
        while (self.pages.items.len > 0) {
            try pages.append(self.next(deps).?);
        }
        return Order{ .allocator = self.allocator, .pages = pages };
    }

    fn next(self: *Order, deps: Rules) ?usize {
        for (self.pages.items, 0..) |page, i| {
            const remove = if (deps.get(page)) |illegal| !self.has(illegal) else true;
            if (remove) {
                return self.pages.orderedRemove(i);
            }
        }
        return null;
    }

    fn has(self: *Order, pages: Pages) bool {
        for (pages.items) |page| {
            if (std.mem.containsAtLeast(usize, self.pages.items, 1, &.{page})) {
                return true;
            }
        }
        return false;
    }
};

pub fn main() !void {
    try answer.timer(solution);
}

fn solution(allocator: Allocator) !void {
    const groups = try Reader.init(allocator).groups();
    const rules = try parseRules(allocator, groups.items[0], true);
    const deps = try parseRules(allocator, groups.items[0], false);
    const orders = try parseOrders(allocator, groups.items[1]);
    answer.part1(usize, 5248, try sum(rules, deps, orders, false));
    answer.part2(usize, 4507, try sum(rules, deps, orders, true));
}

fn parseRules(allocator: Allocator, group: std.ArrayList([]const u8), forward: bool) !Rules {
    var rules = Rules.init(allocator);
    for (group.items) |line| {
        var it = std.mem.splitScalar(u8, line, '|');
        const left = try toInt(it.next().?);
        const right = try toInt(it.next().?);
        const from = if (forward) left else right;
        const to = if (forward) right else left;
        const entry = try rules.getOrPut(from);
        if (!entry.found_existing) {
            entry.value_ptr.* = Pages.init(allocator);
        }
        try entry.value_ptr.*.append(to);
    }
    return rules;
}

fn parseOrders(allocator: Allocator, group: std.ArrayList([]const u8)) !Orders {
    var orders = Orders.init(allocator);
    for (group.items) |line| {
        try orders.append(try Order.init(allocator, line));
    }
    return orders;
}

fn toInt(value: []const u8) !usize {
    return std.fmt.parseInt(usize, value, 10);
}

fn sum(rules: Rules, deps: Rules, orders: Orders, fix: bool) !usize {
    var result: usize = 0;
    for (orders.items) |*order| {
        const valid = try order.valid(rules);
        if (valid and !fix) {
            result += order.*.middle();
        }
        if (!valid and fix) {
            result += (try order.fix(deps)).middle();
        }
    }
    return result;
}
