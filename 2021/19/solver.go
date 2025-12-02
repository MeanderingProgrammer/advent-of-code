package main

import (
	"sync"

	"advent-of-code/commons/go/answer"
	"advent-of-code/commons/go/file"
	"advent-of-code/commons/go/util"
)

type Point struct {
	x int
	y int
	z int
}

func (p1 Point) add(p2 Point) Point {
	return Point{
		x: p1.x + p2.x,
		y: p1.y + p2.y,
		z: p1.z + p2.z,
	}
}

func (p1 Point) subtract(p2 Point) Point {
	return Point{
		x: p1.x - p2.x,
		y: p1.y - p2.y,
		z: p1.z - p2.z,
	}
}

func (p1 Point) distance(p2 Point) int {
	distance := util.Abs(p1.x - p2.x)
	distance += util.Abs(p1.y - p2.y)
	distance += util.Abs(p1.z - p2.z)
	return distance
}

type Rotation func(Point) Point

var rotations = []Rotation{
	func(point Point) Point { return Point{+point.x, +point.y, +point.z} },
	func(point Point) Point { return Point{+point.x, -point.y, -point.z} },
	func(point Point) Point { return Point{+point.x, +point.z, -point.y} },
	func(point Point) Point { return Point{+point.x, -point.z, +point.y} },
	func(point Point) Point { return Point{-point.x, +point.y, -point.z} },
	func(point Point) Point { return Point{-point.x, -point.y, +point.z} },
	func(point Point) Point { return Point{-point.x, +point.z, +point.y} },
	func(point Point) Point { return Point{-point.x, -point.z, -point.y} },
	func(point Point) Point { return Point{+point.y, -point.x, +point.z} },
	func(point Point) Point { return Point{+point.y, +point.x, -point.z} },
	func(point Point) Point { return Point{+point.y, +point.z, +point.x} },
	func(point Point) Point { return Point{+point.y, -point.z, -point.x} },
	func(point Point) Point { return Point{-point.y, +point.x, +point.z} },
	func(point Point) Point { return Point{-point.y, -point.x, -point.z} },
	func(point Point) Point { return Point{-point.y, +point.z, -point.x} },
	func(point Point) Point { return Point{-point.y, -point.z, +point.x} },
	func(point Point) Point { return Point{+point.z, +point.y, -point.x} },
	func(point Point) Point { return Point{+point.z, -point.y, +point.x} },
	func(point Point) Point { return Point{+point.z, +point.x, +point.y} },
	func(point Point) Point { return Point{+point.z, -point.x, -point.y} },
	func(point Point) Point { return Point{-point.z, +point.y, +point.x} },
	func(point Point) Point { return Point{-point.z, -point.y, -point.x} },
	func(point Point) Point { return Point{-point.z, +point.x, -point.y} },
	func(point Point) Point { return Point{-point.z, -point.x, +point.y} },
}

type Points map[Point]bool

func (points Points) offsetWithOverlap(other Points, rotation Rotation, minOverlap int) Transformation {
	offsets := make(map[Point]int)
	for p1 := range points {
		for p2 := range other {
			offset := p1.subtract(rotation(p2))
			offsets[offset]++
			if offsets[offset] >= minOverlap {
				return Transformation{offset: offset, rotation: rotation, exists: true}
			}
		}
	}
	return Transformation{}
}

func (points Points) largestDistance() int {
	result := 0
	for p1 := range points {
		for p2 := range points {
			result = max(result, p1.distance(p2))
		}
	}
	return result
}

type Scanner struct {
	positions Points
	points    Points
}

type Transformation struct {
	rotation Rotation
	offset   Point
	exists   bool
}

func (t Transformation) apply(to, from Points) {
	for point := range from {
		transformed := t.rotation(point).add(t.offset)
		to[transformed] = true
	}
}

type JoinResult struct {
	scanner        Scanner
	transformation Transformation
}

func (s Scanner) joinAllPossible(others []Scanner) []Scanner {
	results := make(chan JoinResult, len(others))
	var wg sync.WaitGroup
	for _, other := range others {
		wg.Add(1)
		go func(other Scanner) {
			defer wg.Done()
			transformation := s.getTransformation(other)
			results <- JoinResult{scanner: other, transformation: transformation}
		}(other)
	}
	wg.Wait()
	close(results)

	var couldNotJoin []Scanner
	for result := range results {
		other, transformation := result.scanner, result.transformation
		if transformation.exists {
			transformation.apply(s.positions, other.positions)
			transformation.apply(s.points, other.points)
		} else {
			couldNotJoin = append(couldNotJoin, other)
		}
	}
	return couldNotJoin
}

func (s Scanner) getTransformation(other Scanner) Transformation {
	for _, rotation := range rotations {
		transformation := s.points.offsetWithOverlap(other.points, rotation, 12)
		if transformation.exists {
			return transformation
		}
	}
	return Transformation{}
}

func main() {
	answer.Timer(solution)
}

func solution() {
	joined := joinAllScanners()
	answer.Part1(512, len(joined.points))
	answer.Part2(16802, joined.positions.largestDistance())
}

func joinAllScanners() Scanner {
	scanners := getScanners()
	joined, unjoinedScanners := scanners[0], scanners[1:]
	for len(unjoinedScanners) > 0 {
		unjoinedScanners = joined.joinAllPossible(unjoinedScanners)
	}
	return joined
}

func getScanners() []Scanner {
	var scanners []Scanner
	for _, rawScanner := range file.Default().Groups() {
		points := make(Points)
		for _, rawPoint := range util.Lines(rawScanner)[1:] {
			coordinates := util.IntCsv(rawPoint)
			point := Point{x: coordinates[0], y: coordinates[1], z: coordinates[2]}
			points[point] = true
		}
		scanner := Scanner{
			// Each scanner is assumed to be at the origin initially
			positions: Points{{0, 0, 0}: true},
			points:    points,
		}
		scanners = append(scanners, scanner)
	}
	return scanners
}
