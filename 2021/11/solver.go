package main

import (
	"advent-of-code/commons/go/answers"
    "advent-of-code/commons/go/conversions"
	"advent-of-code/commons/go/files"
	"advent-of-code/commons/go/parsers"
)

type OctopusGrid struct {
    graph parsers.Graph
    flashed map[parsers.Point]bool
}

func (grid OctopusGrid) runFor(steps int) int {
    flashed := 0
    for i := 0; i < steps; i++ {
        flashed += grid.step()
    }
    return flashed
}

func (grid OctopusGrid) runUntilAll() int {
    target, steps := len(grid.graph.Grid), 1
    for grid.step() != target {
        steps++
    }
    return steps
}

func (grid OctopusGrid) step() int {
    for point := range grid.graph.Grid {
        grid.flash(point)
    }
    flashed := len(grid.flashed)
    for point := range grid.flashed {
        grid.graph.Grid[point] = "0"
        delete(grid.flashed, point)
    }
    return flashed
}

func (grid OctopusGrid) flash(point parsers.Point) {
    if !grid.graph.Contains(point) {
        return
    }
    energy := grid.increment(point)
    if energy > 9 && !grid.flashed[point] {
        grid.flashed[point] = true
        for _, adjacent := range point.Adjacent(true) {
            grid.flash(adjacent)
        }
    }
}

func (grid OctopusGrid) increment(point parsers.Point) int {
    previousValue := grid.graph.Grid[point]
    newValue := conversions.ToInt(previousValue) + 1
    grid.graph.Grid[point] = conversions.ToString(newValue)
    return newValue
}

func main() {
    answers.Part1(1732, getGrid().runFor(100))
    answers.Part2(290, getGrid().runUntilAll())
}

func getGrid() OctopusGrid {
    return OctopusGrid{
        graph: parsers.ConstructGraph(files.Content(), parsers.Character, ""),
        flashed: make(map[parsers.Point]bool),
    }
}
