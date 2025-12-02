package main

import (
	"advent-of-code/commons/go/answer"
	"advent-of-code/commons/go/file"
	"advent-of-code/commons/go/grid"
	"advent-of-code/commons/go/parser"
	"advent-of-code/commons/go/point"
)

type OctopusGrid struct {
	grid.Grid[int]
	flashed map[point.Point]bool
}

func (g OctopusGrid) runFor(steps int) int {
	flashed := 0
	for range steps {
		flashed += g.step()
	}
	return flashed
}

func (g OctopusGrid) runUntilAll() int {
	target, steps := g.Len(), 1
	for g.step() != target {
		steps++
	}
	return steps
}

func (g OctopusGrid) step() int {
	for _, point := range g.Points() {
		g.flash(point)
	}
	flashed := len(g.flashed)
	for point := range g.flashed {
		g.Set(point, 0)
		delete(g.flashed, point)
	}
	return flashed
}

func (g OctopusGrid) flash(p point.Point) {
	if !g.Contains(p) {
		return
	}
	g.Set(p, g.Get(p)+1)
	if g.Get(p) > 9 && !g.flashed[p] {
		g.flashed[p] = true
		for _, adjacent := range p.DiagonalAdjacent() {
			g.flash(adjacent)
		}
	}
}

func main() {
	answer.Timer(solution)
}

func solution() {
	lines := file.Default().Lines()
	answer.Part1(1732, getGrid(lines).runFor(100))
	answer.Part2(290, getGrid(lines).runUntilAll())
}

func getGrid(lines []string) OctopusGrid {
	grid := parser.GridMaker[int]{
		Rows:        lines,
		Splitter:    parser.Character,
		Ignore:      "",
		Transformer: parser.ToInt,
	}.Construct()
	return OctopusGrid{
		Grid:    grid,
		flashed: make(map[point.Point]bool),
	}
}
