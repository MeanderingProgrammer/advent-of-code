const aoc = @import("aoc");
const std = @import("std");

const State = enum {
    start,
    m,
    u,
    l,
    first,
    second,
    d,
    o,
    n,
    apos,
    t,
    do,
    dont,
};

const Parser = struct {
    state: State,
    first: usize,
    second: usize,
    result: usize,
    enabled: bool,
    toggle: bool,

    fn init(toggle: bool) Parser {
        return Parser{
            .state = State.start,
            .first = 0,
            .second = 0,
            .result = 0,
            .enabled = true,
            .toggle = toggle,
        };
    }

    fn add(self: *Parser, command: []const u8) void {
        for (command) |ch| {
            switch (ch) {
                'm' => self.reset(State.m),
                'u' => if (self.state == State.m) {
                    self.set(State.u);
                } else {
                    self.reset(State.start);
                },
                'l' => if (self.state == State.u) {
                    self.set(State.l);
                } else {
                    self.reset(State.start);
                },
                'd' => self.reset(State.d),
                'o' => if (self.state == State.d) {
                    self.set(State.o);
                } else {
                    self.reset(State.start);
                },
                'n' => if (self.state == State.o) {
                    self.set(State.n);
                } else {
                    self.reset(State.start);
                },
                '\'' => if (self.state == State.n) {
                    self.set(State.apos);
                } else {
                    self.reset(State.start);
                },
                't' => if (self.state == State.apos) {
                    self.set(State.t);
                } else {
                    self.reset(State.start);
                },
                ',' => if (self.state == State.first) {
                    self.set(State.second);
                } else {
                    self.reset(State.start);
                },
                '(' => if (self.state == State.l) {
                    self.set(State.first);
                } else if (self.state == State.o) {
                    self.set(State.do);
                } else if (self.state == State.t) {
                    self.set(State.dont);
                } else {
                    self.reset(State.start);
                },
                ')' => {
                    if (self.state == State.second and self.enabled) {
                        self.result = self.result + (self.first * self.second);
                    } else if (self.state == State.do and self.toggle) {
                        self.enabled = true;
                    } else if (self.state == State.dont and self.toggle) {
                        self.enabled = false;
                    }
                    self.reset(State.start);
                },
                '0'...'9' => if (self.state == State.first) {
                    self.first = self.first * 10 + (ch - '0');
                } else if (self.state == State.second) {
                    self.second = self.second * 10 + (ch - '0');
                } else {
                    self.reset(State.start);
                },
                else => self.reset(State.start),
            }
        }
    }

    fn set(self: *Parser, state: State) void {
        self.state = state;
    }

    fn reset(self: *Parser, state: State) void {
        self.state = state;
        self.first = 0;
        self.second = 0;
    }
};

pub fn main() !void {
    try aoc.answer.timer(solution);
}

fn solution() !void {
    const commands = try aoc.reader.Reader.init().read_lines();
    aoc.answer.part1(usize, 159892596, parse_commands(commands, false));
    aoc.answer.part2(usize, 92626942, parse_commands(commands, true));
}

fn parse_commands(commands: std.ArrayList([]const u8), toggle: bool) usize {
    var parser = Parser.init(toggle);
    for (commands.items) |command| {
        parser.add(command);
    }
    return parser.result;
}
