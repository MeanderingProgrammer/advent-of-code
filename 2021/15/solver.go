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
	point parsers.Point
	value int
}

func (path Path) Cost() int {
	return path.value
}

func (path Path) String() *string {
	result := fmt.Sprintf("%v", path.point)
	return &result
}

func (path Path) add(graph graphs.Graph[parsers.Point, int], point parsers.Point) Path {
	return Path{
		point: point,
		value: path.value + graph.Value(point),
	}
}

func main() {
	answers.Part1(656, solve(false))
	answers.Part2(2979, solve(true))
}

func solve(wrap bool) int {
	grid := getGrid(wrap)

	initial := Path{
		point: parsers.Point{X: 0, Y: 0},
		value: 0,
	}

	end := parsers.Point{X: grid.Width, Y: grid.Height}
	done := func(state graphs.State) bool {
		return state.(Path).point == end
	}

	graph := graphs.ConstructGraph(grid)
	nextStates := func(state graphs.State) <-chan graphs.State {
		neighbors := graph.Neighbors(state.(Path).point)
		nextStates := make(chan graphs.State, len(neighbors))
		for _, neighbor := range neighbors {
			nextStates <- state.(Path).add(graph, neighbor)
		}
		close(nextStates)
		return nextStates
	}

	result := graph.Bfs(graphs.Search{
		Initial:    initial,
		Done:       done,
		NextStates: nextStates,
		FirstOnly:  true,
	})
	return result.Completed[0].(Path).value
}

func getGrid(wrap bool) parsers.Grid[int] {
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
					newValue := grid.Get(point) + distance
					if newValue > 9 {
						newValue -= 9
					}
					grid.Set(newPoint, newValue)
				}
			}
		}
	}
	return grid
}

func baseGrid() parsers.Grid[int] {
	toInt := func(point parsers.Point, value string) int {
		return conversions.ToInt(value)
	}
	return parsers.GridMaker[int]{
		Rows:        files.ReadLines(),
		Splitter:    parsers.Character,
		Ignore:      "",
		Transformer: toInt,
	}.Construct()
}
