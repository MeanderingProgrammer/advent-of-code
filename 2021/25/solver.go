package main

import(
    "fmt"
    "io/ioutil"
    "strings"
)

type Position struct {
    x int
    y int
}

type Cucumber int
const (
    East Cucumber = iota
    South
)

func (cucumber Cucumber) target(start Position) Position {
    switch cucumber {
    case East: return Position{x: start.x + 1, y: start.y}
    case South: return Position{x: start.x, y: start.y + 1}
    default: panic(fmt.Sprintf("Unexpected cucumber: %d", cucumber))
    }
}

type Grid struct {
    graph map[Position]Cucumber
    height int
    width int
}

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
    positionsToUpdate := make(map[Position]Position)

    for position, cucumber := range grid.graph {
        if cucumber != toMove {
            continue
        }
        target := cucumber.target(position)
        if target.x >= grid.width {
            target.x = 0
        }
        if target.y >= grid.height {
            target.y = 0
        }
        _, occupied := grid.graph[target]
        if !occupied {
            positionsToUpdate[position] = target
        }
    }

    if len(positionsToUpdate) == 0 {
        return false
    }

    for startPosition, endPosition := range positionsToUpdate {
        delete(grid.graph, startPosition)
        grid.graph[endPosition] = toMove
    }

    return true
}

func (grid Grid) print() {
    for y := 0; y < grid.height; y++ {
        for x := 0; x < grid.width; x++ {
            position := Position{x, y}
            value, exists := grid.graph[position]
            representation := "."
            if exists {
                if value == East {
                    representation = ">"
                } else {
                    representation = "v"
                }
            }
            fmt.Print(representation)
        }
        fmt.Println()
    }
}

func main() {
    cucumbers := getData()
    
    // Part 1: 492
    fmt.Printf("Part 1: %d \n", cucumbers.untilStop())
}

func getData() Grid {
    data, _ := ioutil.ReadFile("data.txt")
    rows := strings.Split(string(data), "\r\n")
    graph := make(map[Position]Cucumber)
    for y, row := range rows {
        for x, value := range row {
            position := Position{x, y}
            if value == '>' {
                graph[position] = East
            } else if value == 'v' {
                graph[position] = South
            }
        }
    }
    return Grid{
        graph: graph,
        height: len(rows),
        width: len(rows[0]),
    }
}
