package main

import (
	"advent-of-code/commons/go/answer"
	"advent-of-code/commons/go/file"
	"advent-of-code/commons/go/point"
	"strings"
)

type Line struct {
	p1 point.Point
	p2 point.Point
}

func (line Line) pointsBetween(includeDiagonal bool) []point.Point {
	var points []point.Point

	xRange := coordinateRange(line.p1.X, line.p2.X)
	yRange := coordinateRange(line.p1.Y, line.p2.Y)

	if len(xRange) == 1 || len(yRange) == 1 {
		// Get vertical / horizontal points
		for _, x := range xRange {
			for _, y := range yRange {
				p := point.Point{X: x, Y: y}
				points = append(points, p)
			}
		}
	} else if includeDiagonal {
		// Get diagonal points if allowed
		for i := 0; i < len(xRange); i++ {
			p := point.Point{X: xRange[i], Y: yRange[i]}
			points = append(points, p)
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
	answer.Timer(solution)
}

func solution() {
	lines := getLines()
	answer.Part1(6666, numPointsWithOverlap(lines, false))
	answer.Part2(19081, numPointsWithOverlap(lines, true))
}

func numPointsWithOverlap(lines []Line, includeDiagonal bool) int {
	frequencies := make(map[point.Point]int)
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

func getLines() []Line {
	return file.Read(func(line string) Line {
		points := strings.Split(line, " -> ")
		return Line{
			p1: point.ConstructPoint(points[0]),
			p2: point.ConstructPoint(points[1]),
		}
	})
}
