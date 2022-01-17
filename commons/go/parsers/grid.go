package parsers

import (
	"advent-of-code/commons/go/utils"
	"fmt"
	"strings"
)

type Point struct {
	X int
	Y int
}

func (point Point) Add(x, y int) Point {
	return Point{
		X: point.X + x,
		Y: point.Y + y,
	}
}

func (point Point) Subtract(x, y int) Point {
	return Point{
		X: point.X - x,
		Y: point.Y - y,
	}
}

func (p1 Point) ManhattanDistance(p2 Point) int {
	difference := p1.Subtract(p2.X, p2.Y)
	return utils.Abs(difference.X) + utils.Abs(difference.Y)
}

func (point Point) Adjacent(includeDiagonal bool) []Point {
	adjacent := []Point{
		{X: point.X - 1, Y: point.Y},
		{X: point.X + 1, Y: point.Y},
		{X: point.X, Y: point.Y - 1},
		{X: point.X, Y: point.Y + 1},
	}
	if includeDiagonal {
		diagonals := []Point{
			{X: point.X + 1, Y: point.Y + 1},
			{X: point.X - 1, Y: point.Y - 1},
			{X: point.X + 1, Y: point.Y - 1},
			{X: point.X - 1, Y: point.Y + 1},
		}
		adjacent = append(adjacent, diagonals...)
	}
	return adjacent
}

func ConstructPoint(s string) Point {
	coords := IntCsv(s)
	return Point{
		X: coords[0],
		Y: coords[1],
	}
}

type Grid[T comparable] struct {
	plane  map[Point]T
	Height int
	Width  int
}

func (grid Grid[T]) Len() int {
	return len(grid.plane)
}

func (grid Grid[T]) Contains(point Point) bool {
	_, exists := grid.plane[point]
	return exists
}

func (grid Grid[T]) Get(point Point) T {
	return grid.plane[point]
}

func (grid *Grid[T]) Set(point Point, value T) {
	if grid.Len() == 0 {
		grid.plane = make(map[Point]T)
	}
	grid.plane[point] = value
	grid.Width = utils.Max(grid.Width, point.X)
	grid.Height = utils.Max(grid.Height, point.Y)
}

func (grid Grid[T]) Delete(point Point) {
	delete(grid.plane, point)
}

func (grid Grid[T]) Points() []Point {
	var points []Point
	for point := range grid.plane {
		points = append(points, point)
	}
	return points
}

func (grid Grid[T]) GetPoints(target T) []Point {
	var points []Point
	for point, value := range grid.plane {
		if value == target {
			points = append(points, point)
		}
	}
	return points
}

func (grid Grid[T]) Print(defaultValue string) {
	for y := 0; y <= grid.Height; y++ {
		for x := 0; x <= grid.Width; x++ {
			point := Point{X: x, Y: y}
			value, exists := grid.plane[point]
			if exists {
				fmt.Print(value)
			} else {
				fmt.Print(defaultValue)
			}
		}
		fmt.Println()
	}
}

type RowSplitter int

const (
	Field RowSplitter = iota
	Character
)

func (splitter RowSplitter) get() func(string) []string {
	switch splitter {
	case Field:
		return fieldSplitter
	case Character:
		return characterSplitter
	default:
		panic(fmt.Sprintf("Unknown splitter: %d", splitter))
	}
}

func fieldSplitter(row string) []string {
	return strings.Fields(row)
}

func characterSplitter(row string) []string {
	return strings.Split(row, "")
}

type ValueParser[T comparable] func(Point, string) T

type GridMaker[T comparable] struct {
	Rows        []string
	Splitter    RowSplitter
	Ignore      string
	Transformer ValueParser[T]
}

func (maker GridMaker[T]) Construct() Grid[T] {
	plane, f := make(map[Point]T), maker.Splitter.get()
	for y, row := range maker.Rows {
		for x, value := range f(row) {
			if !strings.ContainsAny(value, maker.Ignore) {
				point := Point{X: x, Y: y}
				plane[point] = maker.Transformer(point, value)
			}
		}
	}
	return Grid[T]{
		plane:  plane,
		Height: len(maker.Rows) - 1,
		Width:  len(f(maker.Rows[0])) - 1,
	}
}
