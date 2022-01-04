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

func createVertex(point parsers.Point, f func(parsers.Point) interface{}) Vertex {
	return Vertex{
		Point: point,
		Value: f(point),
	}
}

type Graph struct {
	vertices map[Vertex][]Vertex
	grid     parsers.Grid
	f        func(parsers.Point) interface{}
}

func (graph Graph) Neighbors(vertex Vertex) []Vertex {
	return graph.vertices[vertex]
}

func (graph Graph) Print(state State) {
	positions := state.Positions()
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
		vertex := createVertex(point, graph.f)
		value, exists := positions[vertex]
		if !exists {
			value = "."
		}
		return value
	}
}

func ConstructGraph(grid parsers.Grid, f func(parsers.Point) interface{}) Graph {
	vertices := make(map[Vertex][]Vertex)
	for _, point := range grid.Points() {
		var connected []Vertex
		for _, adjacent := range point.Adjacent(false) {
			if grid.Contains(adjacent) {
				connected = append(connected, createVertex(adjacent, f))
			}
		}
		vertices[createVertex(point, f)] = connected
	}
	return Graph{
		vertices: vertices,
		grid:     grid,
		f:        f,
	}
}
