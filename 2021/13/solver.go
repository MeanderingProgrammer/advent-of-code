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

func (fold Fold) apply(point parsers.Point) (parsers.Point, bool) {
    value := point.X
    if fold.direction == Up {
        value = point.Y
    }
    if value > fold.amount {
        result := parsers.Point{X: point.X, Y: point.Y}
        newValue := 2 * fold.amount - value
        if fold.direction == Up {
            result.Y = newValue
        } else {
            result.X = newValue
        }
        return result, true
    } else {
        return point, false
    }
}

func main() {
    grid, folds := getData()

    grid = apply(grid, folds[0])
    answers.Part1(737, grid.Len())

    // Part 2: ZUJUAFHP
    fmt.Println("Part 2")
    for _, fold := range folds[1:] {
        grid = apply(grid, fold)
    }
    grid.Print(".")
}

func apply(grid parsers.Grid, fold Fold) parsers.Grid {
    for _, point := range grid.Points() {
        newPoint, moved := fold.apply(point)
        if moved {
            grid.Delete(point)
            grid.Set(newPoint, "#")
        }
    }
    if fold.direction == Up {
        grid.Height = fold.amount - 1
    } else {
        grid.Width = fold.amount - 1
    }
    return grid
}

func getData() (parsers.Grid, []Fold) {
    dotsInstructions := files.ReadGroups()
    dots, instructions := split(dotsInstructions[0]), split(dotsInstructions[1])

    grid := parsers.Grid{}
    for _, dot := range dots {
        point := getPoint(dot)
        grid.Set(point, "#")
    }

    var folds []Fold
    for _, instruction := range instructions {
        folds = append(folds, getInstruction(instruction))
    }

    return grid, folds
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
