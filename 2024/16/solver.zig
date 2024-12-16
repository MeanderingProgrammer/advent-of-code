const aoc = @import("aoc");
const answer = aoc.answer;
const Direction = aoc.point.Direction;
const Grid = aoc.grid.Grid;
const Point = aoc.point.Point;
const Reader = aoc.reader.Reader;
const Set = aoc.set.Set;
const std = @import("std");
const allocator = std.heap.page_allocator;

const Position = struct {
    point: Point,
    direction: Direction,

    fn init(point: Point, direction: Direction) Position {
        return .{ .point = point, .direction = direction };
    }

    fn next(self: Position) Position {
        return Position.init(self.point.plus(self.direction.point()), self.direction);
    }
};

const State = struct {
    position: Position,
    cost: usize,
    path: std.ArrayList(Point),

    fn init(point: Point, direction: Direction) !State {
        var path = std.ArrayList(Point).init(allocator);
        try path.append(point);
        return .{
            .position = Position.init(point, direction),
            .cost = 0,
            .path = path,
        };
    }

    fn forward(self: State) !State {
        const position = self.position.next();
        var path = try self.path.clone();
        try path.append(position.point);
        return .{
            .position = position,
            .cost = self.cost + 1,
            .path = path,
        };
    }

    fn turn(self: State, direction: Direction) !State {
        const state = State{
            .position = Position.init(self.position.point, direction),
            .cost = self.cost + 1000,
            .path = self.path,
        };
        return try state.forward();
    }
};

const Solution = struct {
    cost: usize,
    seen: Set(Point),
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

    fn solve(self: Maze) !Solution {
        var result = Solution{
            .cost = 0,
            .seen = Set(Point).init(allocator),
        };
        var seen = std.AutoHashMap(Position, usize).init(allocator);
        var q = std.ArrayList(State).init(allocator);
        try q.append(try State.init(self.start, Direction.e));
        while (q.items.len > 0) {
            const state = q.pop();
            if (result.cost > 0 and state.cost > result.cost) {
                continue;
            }
            if (seen.get(state.position)) |cost| {
                if (cost < state.cost) {
                    continue;
                }
            } else {
                try seen.put(state.position, state.cost);
            }
            if (state.position.point.eql(self.end)) {
                result.cost = state.cost;
                for (state.path.items) |point| {
                    try result.seen.add(point);
                }
            } else {
                try self.append(&q, try state.forward());
                try self.append(&q, try state.turn(state.position.direction.left()));
                try self.append(&q, try state.turn(state.position.direction.right()));
            }
        }
        return result;
    }

    fn append(self: Maze, q: *std.ArrayList(State), state: State) !void {
        if (self.grid.get(state.position.point).? != '.') {
            return {};
        }
        try q.insert(get_index(q, state), state);
    }

    fn get_index(q: *std.ArrayList(State), state: State) usize {
        var lo: usize = 0;
        var hi: usize = q.items.len;
        while (lo < hi) {
            const mid = (lo + hi) / 2;
            const value = q.items[mid].cost;
            if (value < state.cost) {
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
    answer.part1(usize, 107512, result.cost);
    answer.part2(usize, 561, result.seen.size());
}
