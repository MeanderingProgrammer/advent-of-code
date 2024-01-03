package main

import (
	"advent-of-code/commons/go/answers"
	"advent-of-code/commons/go/files"
	"advent-of-code/commons/go/parsers"
)

type OctopusGrid struct {
	parsers.Grid[int]
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
	target, steps := grid.Len(), 1
	for grid.step() != target {
		steps++
	}
	return steps
}

func (grid OctopusGrid) step() int {
	for _, point := range grid.Points() {
		grid.flash(point)
	}
	flashed := len(grid.flashed)
	for point := range grid.flashed {
		grid.Set(point, 0)
		delete(grid.flashed, point)
	}
	return flashed
}

func (grid OctopusGrid) flash(point parsers.Point) {
	if !grid.Contains(point) {
		return
	}

	grid.Set(point, grid.Get(point)+1)

	if grid.Get(point) > 9 && !grid.flashed[point] {
		grid.flashed[point] = true
		for _, adjacent := range point.DiagonalAdjacent() {
			grid.flash(adjacent)
		}
	}
}

func main() {
	answers.Part1(1732, getGrid().runFor(100))
	answers.Part2(290, getGrid().runUntilAll())
}

func getGrid() OctopusGrid {
	grid := parsers.GridMaker[int]{
		Rows:        files.ReadLines(),
		Splitter:    parsers.Character,
		Ignore:      "",
		Transformer: parsers.ToInt,
	}.Construct()
	return OctopusGrid{
		Grid:    grid,
		flashed: make(map[parsers.Point]bool),
	}
}
