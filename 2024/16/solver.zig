const std = @import("std");
const aoc = @import("aoc");
const answer = aoc.answer;

const Pair = struct { usize, usize };

const State = struct {
    point: aoc.Point,
    direction: aoc.Direction,

    fn init(point: aoc.Point, direction: aoc.Direction) State {
        return .{
            .point = point,
            .direction = direction,
        };
    }

    fn next(self: State) State {
        return State.init(self.point.plus(self.direction.point()), self.direction);
    }

    fn turn(self: State, left: bool) State {
        const direction = if (left) self.direction.left() else self.direction.right();
        return State.init(self.point, direction);
    }
};

const Maze = struct {
    allocator: std.mem.Allocator,
    grid: aoc.Grid(u8),
    start: aoc.Point,
    end: aoc.Point,

    fn init(allocator: std.mem.Allocator, lines: std.ArrayList([]const u8)) !Maze {
        var grid = aoc.Grid(u8).init(allocator);
        try grid.addLines(lines);
        const start = (try grid.getValues('S')).getLast();
        const end = (try grid.getValues('E')).getLast();
        try grid.put(start, '.');
        try grid.put(end, '.');
        return .{
            .allocator = allocator,
            .grid = grid,
            .start = start,
            .end = end,
        };
    }

    fn solve(self: Maze) !Pair {
        var min_cost: usize = 0;
        var end_seen = aoc.Set(aoc.Point).init(self.allocator);

        const start = State.init(self.start, aoc.Direction.e);

        var distances = std.AutoHashMap(State, usize).init(self.allocator);
        try distances.put(start, 0);

        var start_seen = aoc.Set(aoc.Point).init(self.allocator);
        try start_seen.add(start.point);
        var state_seen = std.AutoHashMap(State, aoc.Set(aoc.Point)).init(self.allocator);
        try state_seen.put(start, start_seen);

        var q = aoc.PriorityQueue(State).init(self.allocator);
        try q.push(start, 0);

        while (!q.isEmpty()) {
            const node = q.pop();
            const current = node.value;
            const current_cost = node.cost;
            if (min_cost > 0 and current_cost > min_cost) {
                continue;
            }
            const current_seen = state_seen.get(current).?;
            if (current.point.eql(self.end)) {
                min_cost = current_cost;
                try end_seen.extend(current_seen);
                continue;
            }
            const neighbors = [3]struct { State, usize }{
                .{ current.next(), 1 },
                .{ current.turn(true).next(), 1001 },
                .{ current.turn(false).next(), 1001 },
            };
            for (neighbors) |neighbor| {
                const next = neighbor[0];
                const cost = current_cost + neighbor[1];
                if (self.grid.get(next.point).? != '.') {
                    continue;
                }
                const entry = try distances.getOrPut(next);
                if (!entry.found_existing or cost < entry.value_ptr.*) {
                    entry.value_ptr.* = cost;
                    try q.push(next, cost);
                    var seen = try current_seen.clone();
                    try seen.add(next.point);
                    try state_seen.put(next, seen);
                } else if (cost == entry.value_ptr.*) {
                    var seen = try current_seen.clone();
                    try seen.add(next.point);
                    try state_seen.getPtr(next).?.extend(seen);
                }
            }
        }

        return .{ min_cost, end_seen.size() };
    }
};

pub fn main() !void {
    try answer.timer(solution);
}

fn solution(c: *aoc.Context) !void {
    const lines = try aoc.Reader.init(c.allocator()).stringLines();
    const maze = try Maze.init(c.allocator(), lines);
    const result = try maze.solve();
    answer.part1(usize, 107512, result[0]);
    answer.part2(usize, 561, result[1]);
}
