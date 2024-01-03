package main

import (
	"advent-of-code/commons/go/answer"
	"advent-of-code/commons/go/file"
	"advent-of-code/commons/go/graph"
	"advent-of-code/commons/go/grid"
	"advent-of-code/commons/go/parser"
	"advent-of-code/commons/go/point"
	"advent-of-code/commons/go/queue"
	"fmt"
)

type Path struct {
	point point.Point
	value int
}

func (path Path) Cost() int {
	return path.value
}

func (path Path) ToString() string {
	return fmt.Sprintf("%v", path.point)
}

func (path Path) add(graph graph.Graph[point.Point, int], p point.Point) Path {
	return Path{
		point: p,
		value: path.value + graph.Value(p),
	}
}

func main() {
	answer.Part1(656, solve(false))
	answer.Part2(2979, solve(true))
}

func solve(wrap bool) int {
	grid := getGrid(wrap)
	g := graph.ConstructGraph(grid)
	result := g.Bfs(graph.Search{
		Initial: Path{
			point: point.Point{X: 0, Y: 0},
			value: 0,
		},
		Done: func(state queue.State) bool {
			return state.(Path).point == point.Point{X: grid.Width, Y: grid.Height}
		},
		NextStates: func(state queue.State) []queue.State {
			nextStates := []queue.State{}
			for _, neighbor := range g.Neighbors(state.(Path).point) {
				nextStates = append(nextStates, state.(Path).add(g, neighbor))
			}
			return nextStates
		},
		FirstOnly: true,
	})
	return result.Completed[0].(Path).value
}

func getGrid(wrap bool) grid.Grid[int] {
	grid := parser.GridMaker[int]{
		Rows:        file.ReadLines(),
		Splitter:    parser.Character,
		Ignore:      "",
		Transformer: parser.ToInt,
	}.Construct()
	if wrap {
		points, baseSize := grid.Points(), grid.Width+1
		for i := 0; i < 5; i++ {
			for j := 0; j < 5; j++ {
				distance := i + j
				if distance == 0 {
					continue
				}
				for _, p := range points {
					newPoint := point.Point{
						X: p.X + (baseSize * i),
						Y: p.Y + (baseSize * j),
					}
					newValue := grid.Get(p) + distance
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
