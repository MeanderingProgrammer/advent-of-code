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

func ConstructVertex(point parsers.Point, grid parsers.Grid, f ValueParser) Vertex {
	return Vertex{
		Point: point,
		Value: f(point, grid.Get(point)),
	}
}

type ValueParser func(parsers.Point, string) interface{}

type Graph struct {
	vertices map[Vertex][]Vertex
	grid     parsers.Grid
	f        ValueParser
}

type Complete func(State) bool
type NextStates func(State) []State

func (graph Graph) Bfs(initial State, done Complete, nextStates NextStates) (int, int) {
	queue, seen, explored := &Queue{initial}, make(map[string]int), 0
	for queue.Len() > 0 {
		explored++
		current := queue.Next().(State)
		if done(current) {
			return current.Cost(), explored
		}
		for _, state := range nextStates(current) {
			encodedState := *state.String()
			seenValue, exists := seen[encodedState]
			if !exists || state.Cost() < seenValue {
				seen[encodedState] = state.Cost()
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

func ConstructGraph(grid parsers.Grid, f ValueParser) Graph {
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
