package point

import (
	"advent-of-code/lib/go/util"
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

func (p Point) Manhattan(other Point) int {
	difference := p.Subtract(other.X, other.Y)
	return util.Abs(difference.X) + util.Abs(difference.Y)
}

func (p Point) Neighbors() []Point {
	return []Point{
		p.Add(-1, 0),
		p.Add(1, 0),
		p.Add(0, -1),
		p.Add(0, 1),
	}
}

func (p Point) AllNeighbors() []Point {
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
