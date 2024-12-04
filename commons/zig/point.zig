pub const Heading = enum {
    w,
    nw,
    n,
    ne,
    e,
    se,
    s,
    sw,
};

pub const Point = struct {
    x: i64,
    y: i64,

    pub fn init(x: i64, y: i64) Point {
        return Point{ .x = x, .y = y };
    }

    pub fn head(self: Point, heading: Heading) Point {
        return switch (heading) {
            Heading.w => self.add(-1, 0),
            Heading.nw => self.add(-1, -1),
            Heading.n => self.add(0, -1),
            Heading.ne => self.add(1, -1),
            Heading.e => self.add(1, 0),
            Heading.se => self.add(1, 1),
            Heading.s => self.add(0, 1),
            Heading.sw => self.add(-1, 1),
        };
    }

    pub fn add(self: Point, dx: i64, dy: i64) Point {
        return Point.init(self.x + dx, self.y + dy);
    }
};
