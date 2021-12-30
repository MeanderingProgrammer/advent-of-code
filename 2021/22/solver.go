package main

import(
    "fmt"
    "io/ioutil"
    "strconv"
    "strings"
)

type Range [2]int

func (r1 Range) overlap(r2 Range) Range {
    maxStart := r1[0]
    if maxStart < r2[0] {
        maxStart = r2[0]
    }

    minEnd := r1[1]
    if minEnd > r2[1] {
        minEnd = r2[1]
    }

    return [2]int{maxStart, minEnd}
}

func (r Range) valid() bool {
    return r[0] <= r[1]
}

func (r Range) length() int {
    return (r[1] - r[0]) + 1
}

type Bound struct {
    count int
    xs Range
    ys Range
    zs Range
}

func (bound Bound) disabledOverlap(newBound Bound) (Bound, bool) {
    xs := bound.xs.overlap(newBound.xs)
    ys := bound.ys.overlap(newBound.ys)
    zs := bound.zs.overlap(newBound.zs)
    if xs.valid() && ys.valid() && zs.valid() {
        return Bound{
            count: -bound.count,
            xs: xs,
            ys: ys,
            zs: zs,
        }, true
    } else {
        return Bound{}, false
    }
}

func (bound Bound) area() int {
    length := bound.xs.length()
    width := bound.ys.length()
    height := bound.zs.length()
    return length * width * height
}

type Bounds []Bound

func (bounds Bounds) disabledOverlappingBounds(newBound Bound) Bounds {
    var overlappingBounds Bounds
    for _, bound := range bounds {
        overlap, exists := bound.disabledOverlap(newBound)
        if exists {
            overlappingBounds = append(overlappingBounds, overlap)
        }
    }
    return overlappingBounds
}

func (bounds Bounds) area() int {
    result := 0
    for _, bound := range bounds {
        area := bound.area()
        result += (area * bound.count)
    }
    return result
}

func main() {
    finalBounds := getFinalBounds()
    // Part 1: 561032
    fmt.Printf("Part 1: %d \n", limitedBoundsArea(finalBounds))
    // Part 2: 1322825263376414
    fmt.Printf("Part 2: %d \n", finalBounds.area())
}

func getFinalBounds() Bounds {
    bounds := getData()
    finalBounds := Bounds{bounds[0]}
    for _, bound := range bounds[1:] {
        finalBounds = append(finalBounds, finalBounds.disabledOverlappingBounds(bound)...)
        if bound.count > 0 {
            finalBounds = append(finalBounds, bound)
        }
    }
    return finalBounds
}

func limitedBoundsArea(bounds Bounds) int {
    limitingBound := Bound{
        xs: [2]int{-50, 50},
        ys: [2]int{-50, 50},
        zs: [2]int{-50, 50},
    }
    boundsDisabled := bounds.disabledOverlappingBounds(limitingBound)
    // Need the negative to handle the fact that this will track the
    // area disabled by our limited bound
    return -boundsDisabled.area()
}

func getData() Bounds {
    data, _ := ioutil.ReadFile("data.txt")
    var bounds Bounds
    for _, bound := range strings.Split(string(data), "\r\n") {
        bounds = append(bounds, parseBound(bound))
    }
    return bounds
}

func parseBound(bound string) Bound {
    enableWhere := strings.Split(bound, " ")
    var count int
    if enableWhere[0] == "on" {
        count = 1
    } else {
        count = -1
    }
    where := strings.Split(enableWhere[1], ",")
    return Bound{
        count: count,
        xs: parseRange(where[0]),
        ys: parseRange(where[1]),
        zs: parseRange(where[2]),
    }
}

func parseRange(rawRange string) Range {
    rangePortion := strings.Split(rawRange, "=")[1]
    bounds := strings.Split(rangePortion, "..")
    return [2]int{toInt(bounds[0]), toInt(bounds[1])}
}

func toInt(value string) int {
    result, _ := strconv.Atoi(value)
    return result
}
