const std = @import("std");

pub fn build(b: *std.Build) void {
    const target = b.standardTargetOptions(.{});
    const optimize = b.standardOptimizeOption(.{});

    const lib = b.addModule("aoc", .{
        .root_source_file = b.path("commons/zig/mod.zig"),
        .target = target,
        .optimize = optimize,
    });

    const solutions = [_]struct { []const u8, []const u8 }{
        .{ "2021", "01" },
        .{ "2024", "01" },
    };

    inline for (solutions) |solution| {
        const year = solution[0];
        const day = solution[1];
        const exe = b.addExecutable(.{
            .name = year ++ "_" ++ day,
            .root_source_file = b.path(year ++ "/" ++ day ++ "/solver.zig"),
            .target = target,
            .optimize = optimize,
        });
        exe.root_module.addImport("aoc", lib);
        b.installArtifact(exe);
        const run_exe = b.addRunArtifact(exe);
        const run_step = b.step(exe.name, "Run " ++ year ++ " " ++ day);
        run_step.dependOn(&run_exe.step);
    }
}
