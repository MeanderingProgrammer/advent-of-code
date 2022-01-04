package graphs

import (
	"advent-of-code/commons/go/parsers"
)

type Graph map[parsers.Point][]parsers.Point

func ConstructGraph(grid parsers.Grid) Graph {
	graph := make(Graph)
	for _, point := range grid.Points() {
		var connected []parsers.Point
		for _, adjacent := range point.Adjacent(false) {
			if grid.Contains(adjacent) {
				connected = append(connected, adjacent)
			}
		}
		graph[point] = connected
	}
	return graph
}
