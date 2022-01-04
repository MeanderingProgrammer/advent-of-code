package graphs

import (
	"advent-of-code/commons/go/parsers"
)

type Vertex struct {
	Point parsers.Point
	Value string
}

type Graph map[Vertex][]Vertex

func ConstructGraph(grid parsers.Grid, f func(parsers.Point) string) Graph {
	graph := make(Graph)
	for _, point := range grid.Points() {
		var connected []Vertex
		for _, adjacent := range point.Adjacent(false) {
			if grid.Contains(adjacent) {
				connected = append(connected, Vertex{Point: adjacent, Value: f(adjacent)})
			}
		}
		graph[Vertex{Point: point, Value: f(point)}] = connected
	}
	return graph
}
