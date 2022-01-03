package parsers

import(
    "advent-of-code/commons/go/conversions"
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

func ConstructPoint(x, y string) Point {
    return Point{
        X: conversions.ToInt(x), 
        Y: conversions.ToInt(y),
    }
}

type Graph struct {
    Grid map[Point]string
    Height int
    Width int
}

func (graph Graph) Contains(point Point) bool {
    _, exists := graph.Grid[point]
    return exists
} 

func (graph Graph) GetPoint(target string) (Point, bool) {
    for point, value := range graph.Grid {
        if value == target {
            return point, true
        }
    }
    return Point{}, false
}

func (graph Graph) Print(defaultValue string) {
    for y := 0; y <= graph.Height; y++ {
        for x := 0; x <= graph.Width; x++ {
            point := Point{X: x, Y: y}
            value, exists := graph.Grid[point]
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
	Field     RowSplitter = iota
	Character
)

func (splitter RowSplitter) get() func(string)[]string {
	switch splitter {
	case Field: return fieldSplitter
	case Character: return characterSplitter
	default: panic(fmt.Sprintf("Unknown splitter: %d", splitter))
	}
}

func fieldSplitter(row string) []string {
	return strings.Fields(row)
}

func characterSplitter(row string) []string {
    return strings.Split(row, "")
}

func ConstructGraph(rawRows string, splitter RowSplitter, ignore string) Graph {
	rows, grid, f := Lines(rawRows), make(map[Point]string), splitter.get()
	for y, row := range rows {
        for x, value := range f(row) {
            if !strings.ContainsAny(value, ignore) {
                grid[Point{X: x, Y: y}] = value
            }
        }
    }
	return Graph{
        Grid: grid, 
        Height: len(rows) - 1, 
        Width: len(f(rows[0])) - 1, 
    }
}
