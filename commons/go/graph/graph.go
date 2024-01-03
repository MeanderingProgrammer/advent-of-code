package graph

import (
	"advent-of-code/commons/go/grid"
	"advent-of-code/commons/go/point"
	"advent-of-code/commons/go/queue"
	"fmt"
	"strings"
)

type Graph[K comparable, V comparable] struct {
	vertices map[K][]K
	grid     grid.Grid[V]
}

type Seen map[string]int

func (seen Seen) updateIfBest(state queue.State) bool {
	encodedState, cost := state.ToString(), state.Cost()
	lowestCost, ok := seen[encodedState]
	if !ok || cost < lowestCost {
		seen[encodedState] = cost
		return true
	} else {
		return false
	}
}

type Search struct {
	Initial    queue.State
	Done       func(queue.State) bool
	NextStates func(queue.State) []queue.State
	FirstOnly  bool
}

type SearchResult struct {
	Completed []queue.State
	Explored  int
}

func (graph Graph[K, V]) Bfs(search Search) SearchResult {
	completed := []queue.State{}
	q := &queue.Queue{search.Initial}
	explored := 0
	seen := make(Seen)
	for !q.Empty() {
		explored++
		current := q.Next()
		if search.Done(current) {
			completed = append(completed, current)
			if search.FirstOnly {
				break
			}
		} else {
			for _, state := range search.NextStates(current) {
				if seen.updateIfBest(state) {
					q.Add(state)
				}
			}
		}
	}
	return SearchResult{
		Completed: completed,
		Explored:  explored,
	}
}

func (graph Graph[K, V]) Neighbors(p K) []K {
	return graph.vertices[p]
}

func (graph Graph[K, V]) Value(p point.Point) V {
	return graph.grid.Get(p)
}

func (graph Graph[K, V]) Print(positions map[point.Point]V) {
	fmt.Println(graph.separator())
	for y := 0; y <= graph.grid.Height; y++ {
		for x := 0; x <= graph.grid.Width; x++ {
			point := point.Point{X: x, Y: y}
			fmt.Print(graph.getValue(positions, point))
		}
		fmt.Println()
	}
	fmt.Println(graph.separator())
}

func (graph Graph[K, V]) separator() string {
	return strings.Repeat("-", graph.grid.Width+1)
}

func (graph Graph[K, V]) getValue(positions map[point.Point]V, p point.Point) interface{} {
	if !graph.grid.Contains(p) {
		return "#"
	} else {
		value, exists := positions[p]
		if exists {
			return value
		} else {
			return "."
		}
	}
}

func ConstructGraph[V comparable](grid grid.Grid[V]) Graph[point.Point, V] {
	vertices := make(map[point.Point][]point.Point)
	for _, p := range grid.Points() {
		var connected []point.Point
		for _, adjacent := range p.Adjacent() {
			if grid.Contains(adjacent) {
				connected = append(connected, adjacent)
			}
		}
		vertices[p] = connected
	}
	return Graph[point.Point, V]{
		vertices: vertices,
		grid:     grid,
	}
}

func ConstructDirectly[K comparable](pairs [][2]K) Graph[K, string] {
	vertices := make(map[K][]K)
	for _, pair := range pairs {
		add(vertices, pair[0], pair[1])
		add(vertices, pair[1], pair[0])
	}
	return Graph[K, string]{
		vertices: vertices,
	}
}

func add[K comparable](graph map[K][]K, start, end K) {
	_, exists := graph[start]
	if exists {
		graph[start] = append(graph[start], end)
	} else {
		graph[start] = []K{end}
	}
}
