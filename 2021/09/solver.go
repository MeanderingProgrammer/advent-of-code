package main

import(
    "fmt"
    "io/ioutil"
    "strconv"
    "strings"
    "sort"
)

type Position struct {
    x int
    y int
}

func (position Position) adjacent() []Position {
    var result []Position
    result = append(result, Position{position.x - 1, position.y})
    result = append(result, Position{position.x + 1, position.y})
    result = append(result, Position{position.x, position.y - 1})
    result = append(result, Position{position.x, position.y + 1})
    return result
}

type HeightPoint struct {
    position Position
    height int
}

func (heightPoint HeightPoint) riskLevel() int {
    return heightPoint.height + 1
}

func (heightPoint HeightPoint) basinSize(heightMap HeightMap) int {
    var basin HeightPoints
    basin = append(basin, heightPoint)

    for i := 0; i < len(basin); i++ {
        for _, adjacent := range basin[i].position.adjacent() {
            adjacentValue, exists := heightMap.mapping[adjacent]
            adjacentHeightPoint := HeightPoint{adjacent, adjacentValue}
            if exists && adjacentValue < 9 && !basin.contains(adjacentHeightPoint) {
                basin = append(basin, adjacentHeightPoint)
            }
        }
    }

    return len(basin)
}

type HeightPoints []HeightPoint

func (heightPoints HeightPoints) contains(heightPoint HeightPoint) bool {
    for _, contained := range heightPoints {
        if contained == heightPoint {
            return true
        }
    }
    return false
}

func (heightPoints HeightPoints) riskLevel() int {
    result := 0
    for _, heightPoint := range heightPoints {
        result += heightPoint.riskLevel()
    }
    return result
}

func (heightPoints HeightPoints) basinSizes(heightMap HeightMap) []int {
    var basinSizes []int
    for _, heightPoint := range heightPoints {
        basinSize := heightPoint.basinSize(heightMap)
        basinSizes = append(basinSizes, basinSize)
    }
    return basinSizes
}

type HeightMap struct {
    mapping map[Position]int
    width int
    height int
}

func (heightMap HeightMap) minimums() HeightPoints {
    var result []HeightPoint
    for position, value := range heightMap.mapping {
        if heightMap.isMinimum(position) {
            result = append(result, HeightPoint{position, value})
        }
    }
    return result
}

func (heightMap HeightMap) isMinimum(position Position) bool {
    value := heightMap.mapping[position]
    for _, adjacent := range position.adjacent() {
        adjacentValue, exists := heightMap.mapping[adjacent]
        if exists && adjacentValue <= value {
            return false
        }
    }
    return true
}

func main() {
    data := getData()

    minimums := data.minimums()
    fmt.Printf("Part 1 = %d \n", minimums.riskLevel())

    basinSizes := minimums.basinSizes(data)
    sort.Sort(sort.Reverse(sort.IntSlice(basinSizes)))
    fmt.Printf("Part 2 = %d \n", basinSizes[0] * basinSizes[1] * basinSizes[2])
}

func getData() HeightMap {
    data, _ := ioutil.ReadFile("data.txt")

    rows := strings.Split(string(data), "\r\n")

    height := len(rows)
    width := len(rows[0])

    mapping := make(map[Position]int)
    for y, row := range rows {
        for x, rawValue := range row {
            position := Position{x, y}
            value, _ := strconv.Atoi(string(rawValue))
            mapping[position] = value            
        }
    }

    
    return HeightMap{mapping, width, height}
}
