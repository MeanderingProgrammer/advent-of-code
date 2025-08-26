const std = @import("std");
const Allocator = std.mem.Allocator;

const aoc = @import("aoc");
const answer = aoc.answer;

const State = struct {
    point: aoc.Point,
    direction: aoc.Direction,

    fn next(self: State) aoc.Point {
        return self.point.plus(self.direction.point());
    }
};

pub fn main() !void {
    try answer.timer(solution);
}

fn solution(c: *aoc.Context) !void {
    const grid = try aoc.Reader.init(c.allocator()).grid();
    const start = (try grid.getValues('^')).getLast();
    var path = (try follow(c.allocator(), grid, start, null)).?;
    answer.part1(usize, 5516, path.size());
    answer.part2(usize, 2008, try obstacles(c.allocator(), grid, start, path));
}

fn follow(allocator: Allocator, grid: aoc.Grid(u8), start: aoc.Point, obstacle: ?aoc.Point) !?aoc.Set(aoc.Point) {
    var seen = aoc.Set(State).init(allocator);
    defer seen.deinit();
    var state = State{ .point = start, .direction = aoc.Direction.n };
    while (grid.get(state.point) != null) {
        if (seen.contains(state)) {
            return null;
        }
        try seen.add(state);
        const next = state.next();
        if (next.eql(obstacle) or (grid.get(next) orelse '.') == '#') {
            state.direction = state.direction.right();
        } else {
            state.point = next;
        }
    }
    var points = aoc.Set(aoc.Point).init(allocator);
    if (obstacle == null) {
        var it = seen.iterator();
        while (it.next()) |s| {
            try points.add(s.point);
        }
    }
    return points;
}

fn obstacles(allocator: Allocator, grid: aoc.Grid(u8), start: aoc.Point, options: aoc.Set(aoc.Point)) !usize {
    var result: usize = 0;
    var it = options.iterator();
    while (it.next()) |point| {
        const p = point.*;
        if (grid.get(p).? != '^' and (try follow(allocator, grid, start, p)) == null) {
            result += 1;
        }
    }
    return result;
}
