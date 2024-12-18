const aoc = @import("aoc");
const answer = aoc.answer;
const Grid = aoc.grid.Grid;
const Direction = aoc.point.Direction;
const Point = aoc.point.Point;
const Reader = aoc.reader.Reader;
const Set = aoc.set.Set;
const std = @import("std");
const allocator = std.heap.page_allocator;

const State = struct {
    point: Point,
    direction: Direction,

    fn next(self: State) Point {
        return self.point.plus(self.direction.point());
    }
};

pub fn main() !void {
    try answer.timer(solution);
}

fn solution() !void {
    var grid = try Reader.init().grid();
    const start = (try grid.get_values('^')).getLast();
    var path = (try follow(&grid, start, null)).?;
    answer.part1(usize, 5516, path.size());
    answer.part2(usize, 2008, try obstacles(&grid, start, path));
}

fn follow(grid: *Grid, start: Point, obstacle: ?Point) !?Set(Point) {
    var seen = Set(State).init(allocator);
    defer seen.deinit();
    var state = State{ .point = start, .direction = Direction.n };
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
    var points = Set(Point).init(allocator);
    if (obstacle == null) {
        var it = seen.iterator();
        while (it.next()) |s| {
            try points.add(s.point);
        }
    }
    return points;
}

fn obstacles(grid: *Grid, start: Point, options: Set(Point)) !usize {
    var result: usize = 0;
    var it = options.iterator();
    while (it.next()) |point| {
        const p = point.*;
        if (grid.get(p).? != '^' and (try follow(grid, start, p)) == null) {
            result += 1;
        }
    }
    return result;
}
