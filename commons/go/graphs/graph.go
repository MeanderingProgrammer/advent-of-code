package graphs

import (
	"advent-of-code/commons/go/parsers"
	"fmt"
	"strings"
)

type Graph[K comparable, V comparable] struct {
	vertices map[K][]K
	grid     parsers.Grid[V]
}

type Complete func(State) bool
type NextStates func(State) <-chan State

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

type Search struct {
	Initial    State
	Done       Complete
	NextStates NextStates
}

func (graph Graph[K, V]) Bfs(search Search) (State, int) {
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

func (graph Graph[K, V]) Neighbors(point K) []K {
	return graph.vertices[point]
}

func (graph Graph[K, V]) Value(point parsers.Point) V {
	return graph.grid.Get(point)
}

func (graph Graph[K, V]) Print(positions map[parsers.Point]V) {
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

func (graph Graph[K, V]) separator() string {
	return strings.Repeat("-", graph.grid.Width+1)
}

func (graph Graph[K, V]) getValue(positions map[parsers.Point]V, point parsers.Point) interface{} {
	if !graph.grid.Contains(point) {
		return "#"
	} else {
		value, exists := positions[point]
		if exists {
			return value
		} else {
			return "."
		}
	}
}

func ConstructGraph[V comparable](grid parsers.Grid[V]) Graph[parsers.Point, V] {
	vertices := make(map[parsers.Point][]parsers.Point)
	for _, point := range grid.Points() {
		var connected []parsers.Point
		for _, adjacent := range point.Adjacent(false) {
			if grid.Contains(adjacent) {
				connected = append(connected, adjacent)
			}
		}
		vertices[point] = connected
	}
	return Graph[parsers.Point, V]{
		vertices: vertices,
		grid:     grid,
	}
}
