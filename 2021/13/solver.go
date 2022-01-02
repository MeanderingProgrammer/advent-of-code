package main

import(
    "advent-of-code/commons/go/answers"
    "advent-of-code/commons/go/conversions"
    "advent-of-code/commons/go/files"
    "advent-of-code/commons/go/parsers"
    "fmt"
    "strings"
)

type Direction int

const (
	Up   Direction = iota
	Left
)

type Fold struct {
    direction Direction
    amount int
}

func (fold Fold) apply(point parsers.Point) parsers.Point {
    value := point.X
    if fold.direction == Up {
        value = point.Y
    }
    if value > fold.amount {
        newValue := 2 * fold.amount - value
        if fold.direction == Up {
            point.Y = newValue
        } else {
            point.X = newValue
        }
    }
    return point
}

func main() {
    graph, folds := getData()

    graph = apply(graph, folds[0])
    answers.Part1(737, len(graph.Grid))

    // Part 2: ZUJUAFHP
    fmt.Println("Part 2")
    for _, fold := range folds[1:] {
        graph = apply(graph, fold)
    }
    graph.Print(".")
}

func apply(graph parsers.Graph,fold Fold) parsers.Graph {
    grid := make(map[parsers.Point]string)
    for point := range graph.Grid {
        grid[fold.apply(point)] = "#"
    }
    result := parsers.Graph{
        Grid: grid, 
        Height: graph.Height,
        Width: graph.Width,
    }
    if fold.direction == Up {
        result.Height = fold.amount - 1
    } else {
        result.Width = fold.amount - 1
    }
    return result
}

func getData() (parsers.Graph, []Fold) {
    dotsInstructions := files.ReadGroups()
    dots, instructions := split(dotsInstructions[0]), split(dotsInstructions[1])

    graph := parsers.Graph{
        Grid: make(map[parsers.Point]string), 
        Height: 0, 
        Width: 0,
    }
    for _, dot := range dots {
        point := getPoint(dot)
        graph.Grid[point] = "#"
        if point.X > graph.Width {
            graph.Width = point.X
        } 
        if point.Y > graph.Height {
            graph.Height = point.Y
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

func getPoint(raw string) parsers.Point {
    parts := strings.Split(raw, ",")
    return parsers.ConstructPoint(parts[0], parts[1])
}

func getInstruction(raw string) Fold {
    parts := strings.Split(raw, "=")
    fold := Fold{Up, conversions.ToInt(parts[1])}
    if strings.HasSuffix(parts[0], "x") {
        fold.direction = Left
    }
    return fold
}
