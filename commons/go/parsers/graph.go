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

func (point Point) Adjacent() []Point {
    return []Point{
        {X: point.X - 1, Y: point.Y},
        {X: point.X + 1, Y: point.Y},
        {X: point.X, Y: point.Y - 1},
        {X: point.X, Y: point.Y + 1},
    }
}

func ConstructPoint(x, y string) Point {
    return Point{
        X: conversions.ToInt(x), 
        Y: conversions.ToInt(y),
    }
}

type Graph struct {
    Grid map[Point]string
    height int
    width int
}

func (graph Graph) GetPoint(target string) (Point, bool) {
    for point, value := range graph.Grid {
        if value == target {
            return point, true
        }
    }
    return Point{}, false
}

func (graph Graph) Print() {
    for y := 0; y < graph.height; y++ {
        for x := 0; x < graph.width; x++ {
            point := Point{X: x, Y: y}
            value := graph.Grid[point]
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

func ConstructGraph(rows []string, splitter RowSplitter) Graph {
	grid, f := make(map[Point]string), splitter.get()
	for y, row := range rows {
        for x, value := range f(row) {
            point := Point{X: x, Y: y}
            grid[point] = value
        }
    }
	return Graph{
        Grid: grid, 
        height: len(rows), 
        width: len(f(rows[0])), 
    }
}
