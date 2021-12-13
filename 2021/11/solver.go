package main

import(
    "fmt"
    "io/ioutil"
    "strconv"
    "strings"
)

type Position struct {
    x int
    y int
}

func (position Position) adjacent() []Position {
    return []Position {
        {position.x - 1, position.y},
        {position.x + 1, position.y},
        {position.x, position.y - 1},
        {position.x, position.y + 1},
        {position.x + 1, position.y + 1},
        {position.x - 1, position.y - 1},
        {position.x + 1, position.y - 1},
        {position.x - 1, position.y + 1},
    }
}

type Octopus struct {
    energy int
    flashed bool
}

type OctopusGrid struct {
    grid map[Position]*Octopus
    rows int
    columns int
}

func (grid OctopusGrid) runFor(steps int) int {
    flashed := 0
    for i := 0; i < steps; i++ {
        flashed += grid.step()
    }
    return flashed
}

func (grid OctopusGrid) runUntilAll() int {
    target := len(grid.grid)
    steps := 1
    for grid.step() != target {
        steps++
    }
    return steps
}

func (grid OctopusGrid) step() int {
    for position := range grid.grid {
        grid.flash(position)
    }

    flashed := 0
    for _, octopus := range grid.grid {
        if octopus.flashed {
            octopus.energy = 0
            octopus.flashed = false
            flashed++
        }
    }
    return flashed
}

func (grid OctopusGrid) flash(position Position) {
    octopus, exists := grid.grid[position]
    if !exists {
        return
    }
    octopus.energy++
    if octopus.energy > 9 && !octopus.flashed {
        octopus.flashed = true
        for _, adjacent := range position.adjacent() {
            grid.flash(adjacent)
        }
    }
}

func (grid OctopusGrid) print() {
    fmt.Println(strings.Repeat("=", 20))
    for y := 0; y < grid.rows; y++ {
        for x := 0; x < grid.columns; x++ {
            position := Position{x, y}
            octopus := grid.grid[position]
            fmt.Print(octopus.energy)
        }
        fmt.Println()
    }
    fmt.Println(strings.Repeat("=", 20))
}

func main() {
    fmt.Printf("Part 1 = %d \n", getData().runFor(100))
    fmt.Printf("Part 2 = %d \n", getData().runUntilAll())
}

func getData() OctopusGrid {
    data, _ := ioutil.ReadFile("data.txt")
    rows := strings.Split(string(data), "\r\n")

    grid := make(map[Position]*Octopus)
    for y, row := range rows {
        for x, rawEnergy := range row {
            position := Position{x, y}
            energy, _ := strconv.Atoi(string(rawEnergy))
            grid[position] = &Octopus{energy, false}
        }
    }
    return OctopusGrid{grid, len(rows), len(rows[0])}
}
