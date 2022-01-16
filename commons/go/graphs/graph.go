package graphs

import (
	"advent-of-code/commons/go/parsers"
	"fmt"
	"strings"
)

type Vertex[V comparable] struct {
	Point parsers.Point
	Value V
}

func ConstructVertex[V comparable](point parsers.Point, grid parsers.Grid[string], f ValueParser[V]) Vertex[V] {
	return Vertex[V]{
		Point: point,
		Value: f(point, grid.Get(point)),
	}
}

type ValueParser[V comparable] func(parsers.Point, string) V

type Graph[V comparable] struct {
	vertices map[Vertex[V]][]Vertex[V]
	grid     parsers.Grid[string]
	f        ValueParser[V]
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

func (graph Graph[V]) Bfs(search Search) (State, int) {
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

func (graph Graph[V]) Neighbors(vertex Vertex[V]) []Vertex[V] {
	return graph.vertices[vertex]
}

func (graph Graph[V]) Print(positions map[Vertex[V]]V) {
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

func (graph Graph[V]) separator() string {
	return strings.Repeat("-", graph.grid.Width+1)
}

func (graph Graph[V]) getValue(positions map[Vertex[V]]V, point parsers.Point) interface{} {
	if !graph.grid.Contains(point) {
		return "#"
	} else {
		vertex := ConstructVertex(point, graph.grid, graph.f)
		value, exists := positions[vertex]
		if exists {
			return value
		} else {
			return "."
		}
	}
}

func ConstructGraph[V comparable](grid parsers.Grid[string], f ValueParser[V]) Graph[V] {
	vertices := make(map[Vertex[V]][]Vertex[V])
	for _, point := range grid.Points() {
		var connected []Vertex[V]
		for _, adjacent := range point.Adjacent(false) {
			if grid.Contains(adjacent) {
				connected = append(connected, ConstructVertex(adjacent, grid, f))
			}
		}
		vertices[ConstructVertex(point, grid, f)] = connected
	}
	return Graph[V]{
		vertices: vertices,
		grid:     grid,
		f:        f,
	}
}
