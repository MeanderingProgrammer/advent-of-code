package main

import (
	"advent-of-code/commons/go/answers"
	"advent-of-code/commons/go/files"
	"advent-of-code/commons/go/parsers"
	"fmt"
)

type Cucumber string

const (
	East  Cucumber = ">"
	South Cucumber = "v"
)

func (cucumber Cucumber) target(start parsers.Point) parsers.Point {
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
	parsers.Grid[Cucumber]
}

type Move struct {
	start parsers.Point
	end   parsers.Point
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
	answers.Part1(492, getGrid().untilStop())
}

func getGrid() Grid {
	grid := parsers.GridMaker[Cucumber]{
		Rows:     files.ReadLines(),
		Splitter: parsers.Character,
		Ignore:   ".",
		Transformer: func(point parsers.Point, value string) Cucumber {
			return Cucumber(value)
		},
	}.Construct()
	return Grid{grid}
}
