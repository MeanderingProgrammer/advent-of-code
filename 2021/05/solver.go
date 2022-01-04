package main

import (
	"advent-of-code/commons/go/answers"
	"advent-of-code/commons/go/files"
	"advent-of-code/commons/go/parsers"
	"strings"
)

type Line struct {
	p1 parsers.Point
	p2 parsers.Point
}

func (line Line) pointsBetween(includeDiagonal bool) []parsers.Point {
	var points []parsers.Point

	xRange := coordinateRange(line.p1.X, line.p2.X)
	yRange := coordinateRange(line.p1.Y, line.p2.Y)

	if len(xRange) == 1 || len(yRange) == 1 {
		// Get vertical / horizontal points
		for _, x := range xRange {
			for _, y := range yRange {
				point := parsers.Point{X: x, Y: y}
				points = append(points, point)
			}
		}
	} else if includeDiagonal {
		// Get diagonal points if allowed
		for i := 0; i < len(xRange); i++ {
			point := parsers.Point{X: xRange[i], Y: yRange[i]}
			points = append(points, point)
		}
	}

	return points
}

func coordinateRange(v1 int, v2 int) []int {
	var result []int
	if v1 < v2 {
		for i := v1; i <= v2; i++ {
			result = append(result, i)
		}
	} else {
		for i := v1; i >= v2; i-- {
			result = append(result, i)
		}
	}
	return result
}

func main() {
	data := getData()

	answers.Part1(6666, numPointsWithOverlap(data, false))
	answers.Part2(19081, numPointsWithOverlap(data, true))
}

func numPointsWithOverlap(lines []Line, includeDiagonal bool) int {
	frequencies := make(map[parsers.Point]int)
	for _, line := range lines {
		for _, point := range line.pointsBetween(includeDiagonal) {
			frequencies[point]++
		}
	}
	totalOverlap := 0
	for _, overlap := range frequencies {
		if overlap >= 2 {
			totalOverlap++
		}
	}
	return totalOverlap
}

func getData() []Line {
	var result []Line
	for _, line := range files.Read(parseLine) {
		result = append(result, line.(Line))
	}
	return result
}

func parseLine(line string) interface{} {
	points := strings.Split(line, " -> ")
	return Line{
		p1: parsePoint(points[0]),
		p2: parsePoint(points[1]),
	}
}

func parsePoint(point string) parsers.Point {
	coords := strings.Split(point, ",")
	return parsers.ConstructPoint(coords[0], coords[1])
}
