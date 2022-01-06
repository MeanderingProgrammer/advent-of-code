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

type Grid struct {
	plane  map[Point]string
	Height int
	Width  int
}

func (grid Grid) Len() int {
	return len(grid.plane)
}

func (grid Grid) Contains(point Point) bool {
	_, exists := grid.plane[point]
	return exists
}

func (grid Grid) Get(point Point) string {
	return grid.plane[point]
}

func (grid *Grid) Set(point Point, value string) {
	if grid.Len() == 0 {
		grid.plane = make(map[Point]string)
	}
	grid.plane[point] = value
	grid.Width = utils.Max(grid.Width, point.X)
	grid.Height = utils.Max(grid.Height, point.Y)
}

func (grid Grid) Delete(point Point) {
	delete(grid.plane, point)
}

func (grid Grid) Points() []Point {
	var points []Point
	for point := range grid.plane {
		points = append(points, point)
	}
	return points
}

func (grid Grid) GetPoints(target string) []Point {
	var points []Point
	for point, value := range grid.plane {
		if value == target {
			points = append(points, point)
		}
	}
	return points
}

func (grid Grid) Print(defaultValue string) {
	for y := 0; y <= grid.Height; y++ {
		for x := 0; x <= grid.Width; x++ {
			point := Point{X: x, Y: y}
			value, exists := grid.plane[point]
			if !exists {
				value = defaultValue
			}
			fmt.Print(value)
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

func ConstructGrid(rows []string, splitter RowSplitter, ignore string) Grid {
	plane, f := make(map[Point]string), splitter.get()
	for y, row := range rows {
		for x, value := range f(row) {
			if !strings.ContainsAny(value, ignore) {
				plane[Point{X: x, Y: y}] = value
			}
		}
	}
	return Grid{
		plane:  plane,
		Height: len(rows) - 1,
		Width:  len(f(rows[0])) - 1,
	}
}
