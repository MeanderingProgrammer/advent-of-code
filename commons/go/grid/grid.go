package grid

import (
	"advent-of-code/commons/go/point"
	"advent-of-code/commons/go/util"
	"fmt"
	"strings"
)

type Grid[T comparable] struct {
	plane  map[point.Point]T
	Height int
	Width  int
}

func New[T comparable](plane map[point.Point]T, height int, width int) Grid[T] {
	return Grid[T]{
		plane:  plane,
		Height: height,
		Width:  width,
	}
}

func (grid Grid[T]) Len() int {
	return len(grid.plane)
}

func (grid Grid[T]) Contains(p point.Point) bool {
	_, exists := grid.plane[p]
	return exists
}

func (grid Grid[T]) Get(p point.Point) T {
	return grid.plane[p]
}

func (grid *Grid[T]) Set(p point.Point, value T) {
	if grid.Len() == 0 {
		grid.plane = make(map[point.Point]T)
	}
	grid.plane[p] = value
	grid.Width = util.Max(grid.Width, p.X)
	grid.Height = util.Max(grid.Height, p.Y)
}

func (grid Grid[T]) Delete(p point.Point) {
	delete(grid.plane, p)
}

func (grid Grid[T]) Points() []point.Point {
	var points []point.Point
	for point := range grid.plane {
		points = append(points, point)
	}
	return points
}

func (grid Grid[T]) GetPoints(target T) []point.Point {
	var points []point.Point
	for point, value := range grid.plane {
		if value == target {
			points = append(points, point)
		}
	}
	return points
}

func (grid Grid[T]) String(defaultValue T) string {
	var rows []string
	for y := 0; y <= grid.Height; y++ {
		var row []string
		for x := 0; x <= grid.Width; x++ {
			p := point.Point{X: x, Y: y}
			value, exists := grid.plane[p]
			if !exists {
				value = defaultValue
			}
			row = append(row, fmt.Sprintf("%v", value))
		}
		rows = append(rows, strings.Join(row, ""))
	}
	return strings.Join(rows, "\n")
}
