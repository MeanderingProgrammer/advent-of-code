package main

import(
    "advent-of-code/commons/go/answers"
    "io/ioutil"
    "strings"
    "strconv"
)

type Point struct {
    x int
    y int
}

type Line struct {
    p1 Point
    p2 Point
}

func (line Line) pointsBetween(includeDiagonal bool) []Point {
    var points []Point

    xRange := coordinateRange(line.p1.x, line.p2.x)
    yRange := coordinateRange(line.p1.y, line.p2.y)

    if len(xRange) == 1 || len(yRange) == 1 {
        // Get vertical / horizontal points
        for _, x := range xRange {
            for _, y := range yRange {
                point := Point{x, y}
                points = append(points, point)
            }
        }
    } else if includeDiagonal && len(xRange) == len(yRange) {
        // Get diagonal points if allow
        for i := 0; i < len(xRange); i++ {
            point := Point{xRange[i], yRange[i]}
            points = append(points, point)
        }
    }

    return points
}

func abs(value int) int {
    if value < 0 {
        return value * -1
    } else {
        return value
    }
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
    frequencies := make(map[Point]int)
    for _, line := range lines {
        for _, point := range line.pointsBetween(includeDiagonal) {
            frequencies[point]++
        }
    }

    totalOverlap := 0
    for _, overlap := range frequencies {
        if overlap >= 2 {
            totalOverlap++;
        }
    }
    return totalOverlap
}

func getData() []Line {
    var result []Line
    data, _ := ioutil.ReadFile("data.txt")
    for _, line := range strings.Split(string(data), "\r\n") {
        result = append(result, parseLine(line))
    }
    return result
}

func parseLine(line string) Line {
    points := strings.Split(line, " -> ")
    return Line{parsePoint(points[0]), parsePoint(points[1])}
}

func parsePoint(point string) Point {
    coords := strings.Split(point, ",")
    x, _ := strconv.Atoi(coords[0])
    y, _ := strconv.Atoi(coords[1])
    return Point{x, y}
}
