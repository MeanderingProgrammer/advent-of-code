const aoc = @import("aoc");
const answer = aoc.answer;
const Direction = aoc.point.Direction;
const Grid = aoc.grid.Grid;
const Point = aoc.point.Point;
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

const Node = struct {
    state: State,
    cost: usize,

    fn init(state: State, cost: usize) Node {
        return .{ .state = state, .cost = cost };
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

        var q = std.ArrayList(Node).init(allocator);
        try q.append(Node.init(start, 0));

        while (q.items.len > 0) {
            const current = q.pop();
            if (min_cost > 0 and current.cost > min_cost) {
                continue;
            }
            const current_seen = state_seen.get(current.state).?;
            if (current.state.point.eql(self.end)) {
                min_cost = current.cost;
                try end_seen.extend(current_seen);
                continue;
            }
            const neightbors = [3]Node{
                Node.init(current.state.next(), current.cost + 1),
                Node.init(current.state.turn(true).next(), current.cost + 1001),
                Node.init(current.state.turn(false).next(), current.cost + 1001),
            };
            for (neightbors) |next| {
                if (self.grid.get(next.state.point).? != '.') {
                    continue;
                }
                const entry = try distances.getOrPut(next.state);
                if (!entry.found_existing or next.cost < entry.value_ptr.*) {
                    entry.value_ptr.* = next.cost;
                    try q.insert(get_index(&q, next.cost), next);
                    var seen = try current_seen.clone();
                    try seen.add(next.state.point);
                    try state_seen.put(next.state, seen);
                } else if (next.cost == entry.value_ptr.*) {
                    var seen = try current_seen.clone();
                    try seen.add(next.state.point);
                    try state_seen.getPtr(next.state).?.extend(seen);
                }
            }
        }

        return .{ min_cost, end_seen.size() };
    }

    fn get_index(q: *std.ArrayList(Node), cost: usize) usize {
        var lo: usize = 0;
        var hi: usize = q.items.len;
        while (lo < hi) {
            const mid = (lo + hi) / 2;
            const value = q.items[mid].cost;
            if (value < cost) {
                hi = mid;
            } else {
                lo = mid + 1;
            }
        }
        return lo;
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
