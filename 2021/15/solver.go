package main

import (
	"advent-of-code/commons/go/answer"
	"advent-of-code/commons/go/file"
	"advent-of-code/commons/go/graph"
	"advent-of-code/commons/go/grid"
	"advent-of-code/commons/go/parser"
	"advent-of-code/commons/go/point"
)

type Path struct {
	point point.Point
	value int
	width int
}

func (path Path) Cost() int {
	return path.value
}

func (path Path) Hash() uint64 {
	return uint64(path.point.Hash(path.width))
}

func (path Path) add(graph graph.Graph[point.Point, int], p point.Point) Path {
	return Path{
		point: p,
		value: path.value + graph.Value(p),
		width: path.width,
	}
}

func main() {
	answer.Timer(solution)
}

func solution() {
	answer.Part1(656, solve(false))
	answer.Part2(2979, solve(true))
}

func solve(wrap bool) int {
	grid := getGrid(wrap)
	g := graph.ConstructGraph(grid)
	result := graph.Search[Path]{
		Initial: Path{
			point: point.Point{X: 0, Y: 0},
			value: 0,
			width: grid.Width,
		},
		Done: func(state Path) bool {
			return state.point == point.Point{X: grid.Width, Y: grid.Height}
		},
		NextStates: func(state Path) []Path {
			nextStates := []Path{}
			for _, neighbor := range g.Neighbors(state.point) {
				nextStates = append(nextStates, state.add(g, neighbor))
			}
			return nextStates
		},
		FirstOnly: true,
	}.Bfs()
	return result.Completed[0].value
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
