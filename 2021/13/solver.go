package main

import (
	"strings"

	"advent-of-code/lib/go/answer"
	"advent-of-code/lib/go/file"
	"advent-of-code/lib/go/grid"
	"advent-of-code/lib/go/point"
	"advent-of-code/lib/go/util"
)

type Direction int

const (
	Up Direction = iota
	Left
)

type Fold struct {
	direction Direction
	amount    int
}

func (fold Fold) apply(p point.Point) (point.Point, bool) {
	value := p.X
	if fold.direction == Up {
		value = p.Y
	}
	if value > fold.amount {
		result := point.Point{X: p.X, Y: p.Y}
		newValue := 2*fold.amount - value
		if fold.direction == Up {
			result.Y = newValue
		} else {
			result.X = newValue
		}
		return result, true
	} else {
		return p, false
	}
}

type PaperGrid struct {
	grid.Grid[string]
}

func (g PaperGrid) apply(fold Fold) PaperGrid {
	for _, p := range g.Points() {
		newPoint, moved := fold.apply(p)
		if moved {
			g.Delete(p)
			g.Set(newPoint, "#")
		}
	}
	if fold.direction == Up {
		g.Height = fold.amount - 1
	} else {
		g.Width = fold.amount - 1
	}
	return g
}

func main() {
	answer.Timer(solution)
}

func solution() {
	grid, folds := getGridFolds()

	grid = grid.apply(folds[0])
	answer.Part1(737, grid.Len())

	for _, fold := range folds[1:] {
		grid = grid.apply(fold)
	}
	expected := []string{
		"####.#..#...##.#..#..##..####.#..#.###..",
		"...#.#..#....#.#..#.#..#.#....#..#.#..#.",
		"..#..#..#....#.#..#.#..#.###..####.#..#.",
		".#...#..#....#.#..#.####.#....#..#.###..",
		"#....#..#.#..#.#..#.#..#.#....#..#.#....",
		"####..##...##...##..#..#.#....#..#.#....",
	}
	answer.Part2("\n"+strings.Join(expected, "\n"), "\n"+grid.String("."))
}

func getGridFolds() (PaperGrid, []Fold) {
	dotsInstructions := file.Default().Groups()
	dots, instructions := util.Lines(dotsInstructions[0]), util.Lines(dotsInstructions[1])

	grid := PaperGrid{}
	for _, dot := range dots {
		point := point.ConstructPoint(dot)
		grid.Set(point, "#")
	}

	var folds []Fold
	for _, instruction := range instructions {
		folds = append(folds, getInstruction(instruction))
	}

	return grid, folds
}

func getInstruction(raw string) Fold {
	parts := strings.Split(raw, "=")
	fold := Fold{Up, util.ToInt(parts[1])}
	if strings.HasSuffix(parts[0], "x") {
		fold.direction = Left
	}
	return fold
}
