package main

import (
	"advent-of-code/commons/go/answers"
	"advent-of-code/commons/go/conversions"
	"advent-of-code/commons/go/files"
	"advent-of-code/commons/go/graphs"
	"advent-of-code/commons/go/parsers"
	"fmt"
)

type Path struct {
	last  graphs.Vertex
	value int
}

func (path Path) Cost() int {
	return path.value
}

func (path Path) String() *string {
	result := fmt.Sprintf("%v", path.last)
	return &result
}

func (path Path) add(vertex graphs.Vertex) Path {
	return Path{
		last:  vertex,
		value: path.value + vertex.Value.(int),
	}
}

func main() {
	answers.Part1(656, solve(false))
	answers.Part2(2979, solve(true))
}

func solve(wrap bool) int {
	grid := getGrid(wrap)

	initial := Path{
		last:  graphs.ConstructVertex(parsers.Point{X: 0, Y: 0}, grid, getType),
		value: 0,
	}

	done := func(state graphs.State) bool {
		path := state.(Path)
		return path.last.Point == parsers.Point{X: grid.Width, Y: grid.Height}
	}

	graph := graphs.ConstructGraph(grid, getType)
	nextStates := func(state graphs.State) []graphs.State {
		var states []graphs.State
		path := state.(Path)
		for _, neighbor := range graph.Neighbors(path.last) {
			states = append(states, path.add(neighbor))
		}
		return states
	}

	cost, _ := graph.Bfs(initial, done, nextStates)
	return cost
}

func getType(position parsers.Point, value string) interface{} {
	return conversions.ToInt(value)
}

func getGrid(wrap bool) parsers.Grid {
	grid := baseGrid()
	if wrap {
		points, baseSize := grid.Points(), grid.Width+1
		for i := 0; i < 5; i++ {
			for j := 0; j < 5; j++ {
				distance := i + j
				if distance == 0 {
					continue
				}
				for _, point := range points {
					newPoint := parsers.Point{
						X: point.X + (baseSize * i),
						Y: point.Y + (baseSize * j),
					}
					newValue := conversions.ToInt(grid.Get(point)) + distance
					if newValue > 9 {
						newValue -= 9
					}
					grid.Set(newPoint, conversions.ToString(newValue))
				}
			}
		}
	}
	return grid
}

func baseGrid() parsers.Grid {
	return parsers.ConstructGrid(files.ReadLines(), parsers.Character, "")
}
