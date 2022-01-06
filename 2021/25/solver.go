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
	parsers.Grid
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
	pointsToUpdate := make(map[parsers.Point]parsers.Point)

	for _, point := range grid.GetPoints(string(toMove)) {
		target := toMove.target(point)
		if target.X > grid.Width {
			target.X = 0
		}
		if target.Y > grid.Height {
			target.Y = 0
		}
		if !grid.Contains(target) {
			pointsToUpdate[point] = target
		}
	}

	for startPoint, endPoint := range pointsToUpdate {
		grid.Delete(startPoint)
		grid.Set(endPoint, string(toMove))
	}

	return len(pointsToUpdate) > 0
}

func main() {
	answers.Part1(492, getGrid().untilStop())
}

func getGrid() Grid {
	return Grid{parsers.ConstructGrid(files.ReadLines(), parsers.Character, ".")}
}
