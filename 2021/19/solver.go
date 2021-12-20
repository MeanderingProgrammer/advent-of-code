package main

import(
    "fmt"
    "io/ioutil"
    "strconv"
    "strings"
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
    distance := 0
    distance += componentDistance(p1.x, p2.x)
    distance += componentDistance(p1.y, p2.y)
    distance += componentDistance(p1.z, p2.z)
    return distance
}

func componentDistance(v1 int, v2 int) int {
    result := v1 - v2
    if result < 0 {
        result *= -1
    }
    return result
}

type Points []Point

func (p1s Points) mostCommonOffset(p2s Points, f func(Point)Point) (Point, int) {
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
            distance := p1.distance(p2)
            if distance > max {
                max = distance
            }
        }
    }
    return max
}

type Scanner struct {
    id int
    positions Points
    points Points
}

type Transformation struct {
    rotation func(Point)Point
    offset Point
}

func (transformation Transformation) apply(point Point) Point {
    return transformation.rotation(point).add(transformation.offset)
}

var rotations = map[string]func(Point)Point {
    "(0,0,1,F)": func (point Point) Point {return Point{ point.x,  point.y, point.z}},
    "(0,0,1,B)": func (point Point) Point {return Point{-point.x, -point.y, point.z}},
    "(0,0,1,L)": func (point Point) Point {return Point{ point.y, -point.x, point.z}},
    "(0,0,1,R)": func (point Point) Point {return Point{-point.y,  point.x, point.z}},

    "(0,0,-1,F)": func (point Point) Point {return Point{-point.x,  point.y, -point.z}},
    "(0,0,-1,B)": func (point Point) Point {return Point{ point.x, -point.y, -point.z}},
    "(0,0,-1,L)": func (point Point) Point {return Point{ point.y,  point.x, -point.z}},
    "(0,0,-1,R)": func (point Point) Point {return Point{-point.y, -point.x, -point.z}},

    "(0,1,0,F)": func (point Point) Point {return Point{ point.x, point.z, -point.y}},
    "(0,1,0,B)": func (point Point) Point {return Point{-point.x, point.z,  point.y}},
    "(0,1,0,L)": func (point Point) Point {return Point{ point.y, point.z,  point.x}},
    "(0,1,0,R)": func (point Point) Point {return Point{-point.y, point.z, -point.x}},

    "(0,-1,0,F)": func (point Point) Point {return Point{ point.x, -point.z,  point.y}},
    "(0,-1,0,B)": func (point Point) Point {return Point{-point.x, -point.z, -point.y}},
    "(0,-1,0,L)": func (point Point) Point {return Point{-point.y, -point.z,  point.x}},
    "(0,-1,0,R)": func (point Point) Point {return Point{ point.y, -point.z, -point.x}},

    "(1,0,0,F)": func (point Point) Point {return Point{point.z, -point.x, -point.y}},
    "(1,0,0,B)": func (point Point) Point {return Point{point.z,  point.x,  point.y}},
    "(1,0,0,L)": func (point Point) Point {return Point{point.z,  point.y, -point.x}},
    "(1,0,0,R)": func (point Point) Point {return Point{point.z, -point.y,  point.x}},

    "(-1,0,0,F)": func (point Point) Point {return Point{-point.z,  point.x, -point.y}},
    "(-1,0,0,B)": func (point Point) Point {return Point{-point.z, -point.x,  point.y}},
    "(-1,0,0,L)": func (point Point) Point {return Point{-point.z,  point.y,  point.x}},
    "(-1,0,0,R)": func (point Point) Point {return Point{-point.z, -point.y, -point.x}},
}

func (s1 *Scanner) join(s2 Scanner) bool {
    transforamtion := s1.getTransformation(s2)
    if transforamtion.rotation == nil {
        return false
    }
    s1.positions = append(s1.positions, transforamtion.offset)
    for _, point := range s2.points {
        transformed := transforamtion.apply(point)
        if !s1.points.contains(transformed) {
            s1.points = append(s1.points, transformed)
        }
    }
    return true
}

func (s1 Scanner) getTransformation(s2 Scanner) Transformation {
    for _, rotation := range rotations {
        offset, frequency := s1.points.mostCommonOffset(s2.points, rotation)
        if frequency >= 12 {
            return Transformation{rotation, offset}
        }
    }
    return Transformation{}
}

func main() {
    joined := joinScanners()

    fmt.Printf("Part 1 = %d \n", len(joined.points))
    fmt.Printf("Part 2 = %d \n", joined.positions.largestDistance())
}

func joinScanners() Scanner {
    scanners := getData()

    scanner, unjoined := scanners[0], scanners[1:]
    previous, current := 0, len(unjoined)
    for previous != current {
        var nextUnjoined []Scanner
        for _, other := range unjoined {
            if !scanner.join(other) {
                nextUnjoined = append(nextUnjoined, other)
            }
        }
        unjoined, previous, current = nextUnjoined, current, len(nextUnjoined)
    }
    return scanner
}

func getData() []Scanner {
    data, _ := ioutil.ReadFile("data.txt")
    var scanners []Scanner
    for i, rawScanner := range strings.Split(string(data), "\r\n\r\n") {
        var points Points
        for _, rawPoint := range strings.Split(rawScanner, "\r\n")[1:] {
            parts := strings.Split(rawPoint, ",")
            point := Point{
                x: toInt(parts[0]),
                y: toInt(parts[1]),
                z: toInt(parts[2]),
            }
            points = append(points, point) 
        }
        scanner := Scanner{
            id: i,
            positions: []Point{
                Point{0,0,0},
            },
            points: points,
        }
        scanners = append(scanners, scanner)
    }
    return scanners
}

func toInt(raw string) int {
    value, _ := strconv.Atoi(raw)
    return value
}
