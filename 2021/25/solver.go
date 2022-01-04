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

type Grid parsers.Graph

func (grid *Grid) untilStop() int {
    moves, didMove := 0, true
    for didMove {
        didMove = grid.step()
        moves++
    }
    return moves
}

func (grid *Grid) step() bool {
    eastMoved := grid.move(East)
    southMoved := grid.move(South)
    return eastMoved || southMoved
}

func (grid *Grid) move(toMove Cucumber) bool {
    pointsToUpdate := make(map[parsers.Point]parsers.Point)

    for point, cucumber := range grid.Grid {
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
        _, occupied := grid.Grid[target]
        if !occupied {
            pointsToUpdate[point] = target
        }
    }

    for startPoint, endPoint := range pointsToUpdate {
        delete(grid.Grid, startPoint)
        grid.Grid[endPoint] = toMove.toString()
    }

    return len(pointsToUpdate) > 0
}

func main() {
    answers.Part1(492, getGrid().untilStop())
}

func getGrid() *Grid {
    graph := Grid(parsers.ConstructGraph(files.Content(), parsers.Character, "."))
    return &graph
}
