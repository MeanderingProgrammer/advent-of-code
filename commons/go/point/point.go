package point

import (
	"advent-of-code/commons/go/util"
)

type Point struct {
	X int
	Y int
}

func (p Point) Add(x, y int) Point {
	return Point{
		X: p.X + x,
		Y: p.Y + y,
	}
}

func (p Point) Subtract(x, y int) Point {
	return Point{
		X: p.X - x,
		Y: p.Y - y,
	}
}

func (p Point) ManhattanDistance(other Point) int {
	difference := p.Subtract(other.X, other.Y)
	return util.Abs(difference.X) + util.Abs(difference.Y)
}

func (p Point) Adjacent() []Point {
	return []Point{
		p.Add(-1, 0),
		p.Add(1, 0),
		p.Add(0, -1),
		p.Add(0, 1),
	}
}

func (p Point) AllAdjacent() []Point {
	return []Point{
		p.Add(-1, 0),
		p.Add(1, 0),
		p.Add(0, -1),
		p.Add(0, 1),
		p.Add(1, 1),
		p.Add(-1, -1),
		p.Add(1, -1),
		p.Add(-1, 1),
	}
}

func (p Point) Hash(width int) int {
	return p.Y*width + p.X
}

func ConstructPoint(s string) Point {
	coords := util.IntCsv(s)
	return Point{
		X: coords[0],
		Y: coords[1],
	}
}
