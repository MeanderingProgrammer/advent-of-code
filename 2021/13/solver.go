package main

import(
    "fmt"
    "io/ioutil"
    "strings"
    "strconv"
)

type Position struct {
    x int
    y int
}

type Direction int

const (
	Up   Direction = iota
	Left
)

type Fold struct {
    direction Direction
    amount int
}

func (fold Fold) apply(position Position) Position {
    value := position.x
    if fold.direction == Up {
        value = position.y
    }
    if value <= fold.amount {
        return position
    } else {
        newValue := 2 * fold.amount - value
        if fold.direction == Up {
            return Position{position.x, newValue}
        } else {
            return Position{newValue, position.y}
        }
    }
}

type Graph struct {
    grid map[Position]string
    rows int
    columns int
}

func (graph Graph) apply(fold Fold) Graph {
    grid := make(map[Position]string)
    for position := range graph.grid {
        grid[fold.apply(position)] = "#"
    }
    if fold.direction == Up {
        return Graph{grid, fold.amount - 1, graph.columns}
    } else {
        return Graph{grid, graph.rows, fold.amount - 1}
    }
}

func (graph Graph) print() {
    for y := 0; y <= graph.rows; y++ {
        for x := 0; x <= graph.columns; x++ {
            position := Position{x, y}
            value, exists := graph.grid[position]
            if !exists {
                value = "."
            }
            fmt.Print(value)
        }
        fmt.Println()
    }
}

func main() {
    graph, folds := getData()

    graph = graph.apply(folds[0])
    // Part 1: 737
    fmt.Printf("Part 1: %d \n", len(graph.grid))
    // Part 2: ZUJUAFHP
    fmt.Println("Part 2")
    for _, fold := range folds[1:] {
        graph = graph.apply(fold)
    }
    graph.print()
}

func getData() (Graph, []Fold) {
    data, _ := ioutil.ReadFile("data.txt")
    dotsInstructions := strings.Split(string(data), "\r\n\r\n")
    dots, instructions := split(dotsInstructions[0]), split(dotsInstructions[1])

    graph := Graph{make(map[Position]string), 0, 0}
    for _, dot := range dots {
        position := getPosition(dot)
        graph.grid[position] = "#"
        if position.x > graph.columns {
            graph.columns = position.x
        } 
        if position.y > graph.rows {
            graph.rows = position.y
        }
    }
    
    var folds []Fold
    for _, instruction := range instructions {
        folds = append(folds, getInstruction(instruction))
    }

    return graph, folds
}

func split(value string) []string {
    return strings.Split(value, "\r\n")
}

func getPosition(raw string) Position {
    parts := strings.Split(raw, ",")
    return Position{convert(parts[0]), convert(parts[1])}
}

func getInstruction(raw string) Fold {
    parts := strings.Split(raw, "=")
    fold := Fold{Up, convert(parts[1])}
    if strings.HasSuffix(parts[0], "x") {
        fold.direction = Left
    }
    return fold
}

func convert(value string) int {
    result, _ := strconv.Atoi(value)
    return result
}
