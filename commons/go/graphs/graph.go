package graphs

import (
	"advent-of-code/commons/go/parsers"
	"fmt"
	"strings"
)

type Vertex struct {
	Point parsers.Point
	Value interface{}
}

func ConstructVertex(point parsers.Point, grid parsers.Grid[string], f ValueParser) Vertex {
	return Vertex{
		Point: point,
		Value: f(point, grid.Get(point)),
	}
}

type ValueParser func(parsers.Point, string) interface{}

type Graph struct {
	vertices map[Vertex][]Vertex
	grid     parsers.Grid[string]
	f        ValueParser
}

type Complete func(State) bool
type NextStates func(State) <-chan State

type Search struct {
	Initial    State
	Done       Complete
	NextStates NextStates
}

type Seen map[string]int

func (seen Seen) updateIfBest(state State) bool {
	encodedState, cost := *state.String(), state.Cost()
	lowestCost, exists := seen[encodedState]
	if !exists || cost < lowestCost {
		seen[encodedState] = cost
		return true
	} else {
		return false
	}
}

func (graph Graph) Bfs(search Search) (State, int) {
	queue, seen, explored := &Queue{search.Initial}, make(Seen), 0
	for !queue.Empty() {
		explored++
		current := queue.Next()
		if search.Done(current) {
			return current, explored
		}
		for state := range search.NextStates(current) {
			if seen.updateIfBest(state) {
				queue.Add(state)
			}
		}
	}
	panic("Could not find a solution")
}

func (graph Graph) Neighbors(vertex Vertex) []Vertex {
	return graph.vertices[vertex]
}

func (graph Graph) Print(positions map[Vertex]interface{}) {
	fmt.Println(graph.separator())
	for y := 0; y <= graph.grid.Height; y++ {
		for x := 0; x <= graph.grid.Width; x++ {
			point := parsers.Point{X: x, Y: y}
			fmt.Print(graph.getValue(positions, point))
		}
		fmt.Println()
	}
	fmt.Println(graph.separator())
}

func (graph Graph) separator() string {
	return strings.Repeat("-", graph.grid.Width+1)
}

func (graph Graph) getValue(positions map[Vertex]interface{}, point parsers.Point) interface{} {
	if !graph.grid.Contains(point) {
		return "#"
	} else {
		vertex := ConstructVertex(point, graph.grid, graph.f)
		value, exists := positions[vertex]
		if !exists {
			value = "."
		}
		return value
	}
}

func ConstructGraph(grid parsers.Grid[string], f ValueParser) Graph {
	vertices := make(map[Vertex][]Vertex)
	for _, point := range grid.Points() {
		var connected []Vertex
		for _, adjacent := range point.Adjacent(false) {
			if grid.Contains(adjacent) {
				connected = append(connected, ConstructVertex(adjacent, grid, f))
			}
		}
		vertices[ConstructVertex(point, grid, f)] = connected
	}
	return Graph{
		vertices: vertices,
		grid:     grid,
		f:        f,
	}
}
