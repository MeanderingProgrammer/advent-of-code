const std = @import("std");
const Allocator = std.mem.Allocator;
const aoc = @import("aoc");
const answer = aoc.answer;
const Reader = aoc.reader.Reader;

const State = enum {
    start,
    m,
    mu,
    mul,
    first,
    second,
    d,
    do,
    don,
    don_,
    don_t,
    on,
    off,
};

const Move = struct {
    from: State,
    to: State,

    fn init(from: State, to: State) Move {
        return .{
            .from = from,
            .to = to,
        };
    }
};

const Parser = struct {
    state: State,
    first: usize,
    second: usize,
    result: usize,
    enabled: bool,
    toggle: bool,

    fn init(toggle: bool) Parser {
        return .{
            .state = State.start,
            .first = 0,
            .second = 0,
            .result = 0,
            .enabled = true,
            .toggle = toggle,
        };
    }

    fn add(self: *Parser, ch: u8) void {
        switch (ch) {
            'm' => self.reset(State.m),
            'u' => self.transition(&.{Move.init(State.m, State.mu)}),
            'l' => self.transition(&.{Move.init(State.mu, State.mul)}),
            'd' => self.reset(State.d),
            'o' => self.transition(&.{Move.init(State.d, State.do)}),
            'n' => self.transition(&.{Move.init(State.do, State.don)}),
            '\'' => self.transition(&.{Move.init(State.don, State.don_)}),
            't' => self.transition(&.{Move.init(State.don_, State.don_t)}),
            ',' => self.transition(&.{Move.init(State.first, State.second)}),
            '(' => self.transition(&.{
                Move.init(State.mul, State.first),
                Move.init(State.do, State.on),
                Move.init(State.don_t, State.off),
            }),
            ')' => {
                if (self.state == State.second and self.enabled) {
                    self.result = self.result + (self.first * self.second);
                } else if (self.state == State.on and self.toggle) {
                    self.enabled = true;
                } else if (self.state == State.off and self.toggle) {
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

    fn reset(self: *Parser, state: State) void {
        self.state = state;
        self.first = 0;
        self.second = 0;
    }

    fn transition(self: *Parser, moves: []const Move) void {
        for (moves) |move| {
            if (self.state == move.from) {
                self.state = move.to;
                return;
            }
        }
        self.reset(State.start);
    }
};

pub fn main() !void {
    try answer.timer(solution);
}

fn solution(allocator: Allocator) !void {
    const commands = try Reader.init(allocator).stringLines();
    answer.part1(usize, 159892596, parseCommands(commands, false));
    answer.part2(usize, 92626942, parseCommands(commands, true));
}

fn parseCommands(commands: std.ArrayList([]const u8), toggle: bool) usize {
    var parser = Parser.init(toggle);
    for (commands.items) |command| {
        for (command) |ch| {
            parser.add(ch);
        }
    }
    return parser.result;
}
