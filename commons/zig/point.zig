pub const Direction = enum {
    n,
    e,
    s,
    w,

    pub fn point(self: Direction) Point {
        return switch (self) {
            Direction.n => Point.init(0, -1),
            Direction.e => Point.init(1, 0),
            Direction.s => Point.init(0, 1),
            Direction.w => Point.init(-1, 0),
        };
    }

    pub fn clockwise(self: Direction) Direction {
        return switch (self) {
            Direction.n => Direction.e,
            Direction.e => Direction.s,
            Direction.s => Direction.w,
            Direction.w => Direction.n,
        };
    }
};

pub const Heading = enum {
    w,
    nw,
    n,
    ne,
    e,
    se,
    s,
    sw,

    pub fn point(self: Heading) Point {
        return switch (self) {
            Heading.w => Point.init(-1, 0),
            Heading.nw => Point.init(-1, -1),
            Heading.n => Point.init(0, -1),
            Heading.ne => Point.init(1, -1),
            Heading.e => Point.init(1, 0),
            Heading.se => Point.init(1, 1),
            Heading.s => Point.init(0, 1),
            Heading.sw => Point.init(-1, 1),
        };
    }
};

pub const Point = struct {
    x: i64,
    y: i64,

    pub fn init(x: i64, y: i64) Point {
        return Point{ .x = x, .y = y };
    }

    pub fn negate(self: Point) Point {
        return Point.init(-self.x, -self.y);
    }

    pub fn times(self: Point, scalar: i64) Point {
        return Point.init(self.x * scalar, self.y * scalar);
    }

    pub fn plus(self: Point, other: Point) Point {
        return Point.init(self.x + other.x, self.y + other.y);
    }

    pub fn minus(self: Point, other: Point) Point {
        return Point.init(self.x - other.x, self.y - other.y);
    }
};
