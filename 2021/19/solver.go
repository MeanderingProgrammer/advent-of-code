package main

import (
	"advent-of-code/commons/go/answers"
	"advent-of-code/commons/go/files"
	"advent-of-code/commons/go/parsers"
	"advent-of-code/commons/go/utils"
)

type Point struct {
	x int
	y int
	z int
}

func (p1 Point) offset(p2 Point) Point {
	return Point{
		x: p1.x - p2.x,
		y: p1.y - p2.y,
		z: p1.z - p2.z,
	}
}

func (p1 Point) add(p2 Point) Point {
	return Point{
		x: p1.x + p2.x,
		y: p1.y + p2.y,
		z: p1.z + p2.z,
	}
}

func (p1 Point) distance(p2 Point) int {
	distance := utils.Abs(p1.x - p2.x)
	distance += utils.Abs(p1.y - p2.y)
	distance += utils.Abs(p1.z - p2.z)
	return distance
}

type Points []Point

func (p1s Points) mostCommonOffset(p2s Points, f func(Point) Point) (Point, int) {
	mostCommonOffset, frequency, offsets := Point{}, 0, make(map[Point]int)
	for _, p1 := range p1s {
		for _, p2 := range p2s {
			offset := p1.offset(f(p2))
			offsets[offset]++
			if offsets[offset] > frequency {
				mostCommonOffset = offset
				frequency = offsets[offset]
			}
		}
	}
	return mostCommonOffset, frequency
}

func (points Points) contains(target Point) bool {
	for _, point := range points {
		if point == target {
			return true
		}
	}
	return false
}

func (points Points) largestDistance() int {
	max := 0
	for _, p1 := range points {
		for _, p2 := range points {
			max = utils.Max(max, p1.distance(p2))
		}
	}
	return max
}

type Scanner struct {
	positions Points
	points    Points
}

type Transformation struct {
	rotation func(Point) Point
	offset   Point
}

func (transformation Transformation) apply(point Point) Point {
	return transformation.rotation(point).add(transformation.offset)
}

var rotations = []func(Point) Point{
	func(point Point) Point { return Point{point.x, point.y, point.z} },
	func(point Point) Point { return Point{-point.x, -point.y, point.z} },
	func(point Point) Point { return Point{point.y, -point.x, point.z} },
	func(point Point) Point { return Point{-point.y, point.x, point.z} },

	func(point Point) Point { return Point{-point.x, point.y, -point.z} },
	func(point Point) Point { return Point{point.x, -point.y, -point.z} },
	func(point Point) Point { return Point{point.y, point.x, -point.z} },
	func(point Point) Point { return Point{-point.y, -point.x, -point.z} },

	func(point Point) Point { return Point{point.x, point.z, -point.y} },
	func(point Point) Point { return Point{-point.x, point.z, point.y} },
	func(point Point) Point { return Point{point.y, point.z, point.x} },
	func(point Point) Point { return Point{-point.y, point.z, -point.x} },

	func(point Point) Point { return Point{point.x, -point.z, point.y} },
	func(point Point) Point { return Point{-point.x, -point.z, -point.y} },
	func(point Point) Point { return Point{-point.y, -point.z, point.x} },
	func(point Point) Point { return Point{point.y, -point.z, -point.x} },

	func(point Point) Point { return Point{point.z, -point.x, -point.y} },
	func(point Point) Point { return Point{point.z, point.x, point.y} },
	func(point Point) Point { return Point{point.z, point.y, -point.x} },
	func(point Point) Point { return Point{point.z, -point.y, point.x} },

	func(point Point) Point { return Point{-point.z, point.x, -point.y} },
	func(point Point) Point { return Point{-point.z, -point.x, point.y} },
	func(point Point) Point { return Point{-point.z, point.y, point.x} },
	func(point Point) Point { return Point{-point.z, -point.y, -point.x} },
}

func (s1 *Scanner) join(s2 Scanner) bool {
	transformation, exists := s1.getTransformation(s2)
	if !exists {
		return false
	}
	s1.positions = append(s1.positions, transformation.offset)
	for _, point := range s2.points {
		transformed := transformation.apply(point)
		if !s1.points.contains(transformed) {
			s1.points = append(s1.points, transformed)
		}
	}
	return true
}

func (s1 Scanner) getTransformation(s2 Scanner) (Transformation, bool) {
	for _, rotation := range rotations {
		offset, frequency := s1.points.mostCommonOffset(s2.points, rotation)
		if frequency >= 12 {
			return Transformation{rotation, offset}, true
		}
	}
	return Transformation{}, false
}

func main() {
	joined := joinScanners()

	answers.Part1(512, len(joined.points))
	answers.Part2(16802, joined.positions.largestDistance())
}

func joinScanners() Scanner {
	scanners := getScanners()
	joined, unjoinedScanners := scanners[0], scanners[1:]
	for len(unjoinedScanners) > 0 {
		var nextUnjoined []Scanner
		for _, unjoined := range unjoinedScanners {
			if !joined.join(unjoined) {
				nextUnjoined = append(nextUnjoined, unjoined)
			}
		}
		unjoinedScanners = nextUnjoined
	}
	return joined
}

func getScanners() []Scanner {
	var scanners []Scanner
	for _, rawScanner := range files.ReadGroups() {
		var points Points
		for _, rawPoint := range parsers.Lines(rawScanner)[1:] {
			coordinates := parsers.IntCsv(rawPoint)
			point := Point{
				x: coordinates[0],
				y: coordinates[1],
				z: coordinates[2],
			}
			points = append(points, point)
		}
		scanner := Scanner{
			// Each scanner is assumed to be at the origin relative to itself
			positions: []Point{
				{0, 0, 0},
			},
			points: points,
		}
		scanners = append(scanners, scanner)
	}
	return scanners
}
