const aoc = @import("aoc");
const answer = aoc.answer;
const Direction = aoc.point.Direction;
const Grid = aoc.grid.Grid;
const Point = aoc.point.Point;
const PriorityQueue = aoc.queue.PriorityQueue;
const Reader = aoc.reader.Reader;
const Set = aoc.set.Set;
const std = @import("std");
const allocator = std.heap.page_allocator;

const State = struct {
    point: Point,
    direction: Direction,

    fn init(point: Point, direction: Direction) State {
        return .{ .point = point, .direction = direction };
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
    grid: Grid,
    start: Point,
    end: Point,

    fn init(lines: std.ArrayList([]const u8)) !Maze {
        var grid = try Grid.init(lines);
        const start = (try grid.get_values('S')).getLast();
        const end = (try grid.get_values('E')).getLast();
        try grid.set(start, '.');
        try grid.set(end, '.');
        return .{
            .grid = grid,
            .start = start,
            .end = end,
        };
    }

    fn solve(self: Maze) !struct { usize, usize } {
        var min_cost: usize = 0;
        var end_seen = Set(Point).init(allocator);

        const start = State.init(self.start, Direction.e);

        var distances = std.AutoHashMap(State, usize).init(allocator);
        try distances.put(start, 0);

        var start_seen = Set(Point).init(allocator);
        try start_seen.add(start.point);
        var state_seen = std.AutoHashMap(State, Set(Point)).init(allocator);
        try state_seen.put(start, start_seen);

        var q = PriorityQueue(State).init(allocator);
        try q.push(start, 0);

        while (!q.is_empty()) {
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

fn solution() !void {
    const lines = try Reader.init().string_lines();
    const maze = try Maze.init(lines);
    const result = try maze.solve();
    answer.part1(usize, 107512, result[0]);
    answer.part2(usize, 561, result[1]);
}
