package main

import (
	"fmt"

	"advent-of-code/lib/go/answer"
	"advent-of-code/lib/go/file"
	"advent-of-code/lib/go/grid"
	"advent-of-code/lib/go/parser"
	"advent-of-code/lib/go/point"
)

type Cucumber string

const (
	East  Cucumber = ">"
	South Cucumber = "v"
)

func (cucumber Cucumber) target(start point.Point) point.Point {
	switch cucumber {
	case East:
		return start.Add(1, 0)
	case South:
		return start.Add(0, 1)
	default:
		panic(fmt.Sprintf("Unexpected cucumber: %s", cucumber))
	}
}

type Grid struct {
	grid.Grid[Cucumber]
}

type Move struct {
	start point.Point
	end   point.Point
}

func (grid Grid) untilStop() int {
	moves, didMove := 0, true
	for didMove {
		didMove = grid.step()
		moves++
	}
	return moves
}

func (grid Grid) step() bool {
	eastMoved := grid.move(East)
	southMoved := grid.move(South)
	return eastMoved || southMoved
}

func (grid Grid) move(toMove Cucumber) bool {
	var moves []Move

	for _, point := range grid.GetPoints(toMove) {
		target := toMove.target(point)
		if target.X > grid.Width {
			target.X = 0
		}
		if target.Y > grid.Height {
			target.Y = 0
		}
		if !grid.Contains(target) {
			move := Move{start: point, end: target}
			moves = append(moves, move)
		}
	}

	for _, move := range moves {
		grid.Delete(move.start)
		grid.Set(move.end, toMove)
	}

	return len(moves) > 0
}

func main() {
	answer.Timer(solution)
}

func solution() {
	lines := file.Default().Lines()
	answer.Part1(492, getGrid(lines).untilStop())
}

func getGrid(lines []string) Grid {
	grid := parser.GridMaker[Cucumber]{
		Rows:     lines,
		Splitter: parser.Character,
		Ignore:   ".",
		Transformer: func(point point.Point, value string) Cucumber {
			return Cucumber(value)
		},
	}.Construct()
	return Grid{grid}
}
