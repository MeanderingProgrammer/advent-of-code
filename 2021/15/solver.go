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
	vertex graphs.Vertex
	value  int
}

func (path Path) Cost() int {
	return path.value
}

func (path Path) String() *string {
	result := fmt.Sprintf("%v", path.vertex)
	return &result
}

func (path Path) add(vertex graphs.Vertex) Path {
	return Path{
		vertex: vertex,
		value:  path.value + vertex.Value.(int),
	}
}

func main() {
	answers.Part1(656, solve(false))
	answers.Part2(2979, solve(true))
}

func solve(wrap bool) int {
	grid := getGrid(wrap)

	initial := Path{
		vertex: graphs.ConstructVertex(parsers.Point{X: 0, Y: 0}, grid, getType),
		value:  0,
	}

	end := parsers.Point{X: grid.Width, Y: grid.Height}
	done := func(state graphs.State) bool {
		return state.(Path).vertex.Point == end
	}

	graph := graphs.ConstructGraph(grid, getType)
	nextStates := func(state graphs.State) <-chan graphs.State {
		neighbors := graph.Neighbors(state.(Path).vertex)
		nextStates := make(chan graphs.State, len(neighbors))
		for _, neighbor := range neighbors {
			nextStates <- state.(Path).add(neighbor)
		}
		close(nextStates)
		return nextStates
	}

	endState, _ := graph.Bfs(graphs.Search{
		Initial:    initial,
		Done:       done,
		NextStates: nextStates,
	})
	return endState.(Path).value
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
