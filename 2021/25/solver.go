package main

import(
    "advent-of-code/commons/go/answers"
    "advent-of-code/commons/go/files"
    "advent-of-code/commons/go/parsers"
    "fmt"
)

type Cucumber int
const (
    East Cucumber = iota
    South
)

func (cucumber Cucumber) toString() string {
    switch cucumber {
    case East: return ">"
    case South: return "v"
    default: panic(fmt.Sprintf("Unexpected cucumber: %d", cucumber))
    }
}

func (cucumber Cucumber) target(start parsers.Point) parsers.Point {
    switch cucumber {
    case East: return start.Add(1, 0)
    case South: return start.Add(0, 1)
    default: panic(fmt.Sprintf("Unexpected cucumber: %d", cucumber))
    }
}

func main() {
    answers.Part1(492, untilStop(getGrid()))
}

func untilStop(grid parsers.Grid) int {
    moves, didMove := 0, true
    for didMove {
        didMove = step(grid)
        moves++
    }
    return moves
}

func step(grid parsers.Grid) bool {
    eastMoved := move(grid, East)
    southMoved := move(grid, South)
    return eastMoved || southMoved
}

func move(grid parsers.Grid, toMove Cucumber) bool {
    pointsToUpdate := make(map[parsers.Point]parsers.Point)

    for _, point := range grid.Points() {
        cucumber := grid.Get(point)
        if cucumber != toMove.toString() {
            continue
        }
        target := toMove.target(point)
        if target.X > grid.Width {
            target.X = 0
        }
        if target.Y > grid.Height {
            target.Y = 0
        }
        if !grid.Contains(target) {
            pointsToUpdate[point] = target
        }
    }

    for startPoint, endPoint := range pointsToUpdate {
        grid.Delete(startPoint)
        grid.Set(endPoint, toMove.toString())
    }

    return len(pointsToUpdate) > 0
}

func getGrid() parsers.Grid {
    return parsers.ConstructGrid(files.ReadLines(), parsers.Character, ".")
}
