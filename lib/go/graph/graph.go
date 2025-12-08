package graph

import (
	"fmt"
	"strings"

	"advent-of-code/lib/go/grid"
	"advent-of-code/lib/go/point"
)

type Graph[K comparable, V comparable] struct {
	vertices map[K][]K
	grid     grid.Grid[V]
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

func (graph Graph[K, V]) getValue(positions map[point.Point]V, p point.Point) any {
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
		for _, neighbor := range p.Neighbors() {
			if grid.Contains(neighbor) {
				connected = append(connected, neighbor)
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
