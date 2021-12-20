package main

import(
    "fmt"
    "io/ioutil"
    "strconv"
    "strings"
)

const Boarder = 5

type Enhancer string

func (enhancer Enhancer) edgeBehavior(time int) bool {
    if enhancer[0] == '.' {
        return false
    } else if enhancer[len(enhancer) - 1] == '#' || time % 2 == 1 {
        return true
    } else {
        return false
    }
}

type Position struct {
    x int
    y int
}

type Bounds struct {
    minX int
    maxX int
    minY int
    maxY int
}

func (bounds Bounds) out(position Position) bool {
    return position.x < bounds.minX  || 
        position.x > bounds.maxX ||
        position.y < bounds.minY ||
        position.y > bounds.maxY
}

type Graph struct {
    grid map[Position]bool
    times int
}

func (graph Graph) enhance(enhancer Enhancer) Graph {
    enhanced := make(map[Position]bool)
    bounds := graph.getBounds()
    for y := bounds.minY - Boarder; y <= bounds.maxY + Boarder; y++ {
        for x := bounds.minX - Boarder; x <= bounds.maxX + Boarder; x++ {
            position := Position{x, y}
            if graph.enhanceValue(position, enhancer, bounds) {
                enhanced[position] = true
            }
        }
    } 
    return Graph{enhanced, graph.times + 1}
}

func (graph Graph) enhanceValue(position Position, enhancer Enhancer, bounds Bounds) bool {
    var indexCode strings.Builder
    for y := -1; y <= 1; y++ {
        for x := -1; x <= 1; x++ {
            surrounding := Position{position.x + x, position.y + y}
            value := graph.grid[surrounding]
            if value || (bounds.out(surrounding) && enhancer.edgeBehavior(graph.times)) {
                indexCode.WriteString("1")
            } else {
                indexCode.WriteString("0")
            }
        }
    }
    index, _ := strconv.ParseInt(indexCode.String(), 2, 64)
    return enhancer[index] == '#'
}

func (graph Graph) getBounds() Bounds {
    minX, minY, maxX, maxY := 0, 0, 0, 0
    for position := range graph.grid {
        x := position.x
        if x < minX {
            minX = x
        } else if x > maxX {
            maxX = x
        }

        y := position.y
        if y < minY {
            minY = y
        } else if y > maxY {
            maxY = y
        }

    }
    return Bounds{
        minX: minX,
        maxX: maxX,
        minY: minY,
        maxY: maxY,
    }
}

func (graph Graph) print() {
    bounds := graph.getBounds()
    for y := bounds.minY; y <= bounds.maxY; y++ {
        for x := bounds.minX; x <= bounds.maxX; x++ {
            position := Position{x, y}
            value := graph.grid[position]
            if value {
                fmt.Print("#")
            } else {
                fmt.Print(".")
            }
        }
        fmt.Println()
    }
}

func main() {
    fmt.Printf("Part 1 = %d \n", litAfter(2))
    fmt.Printf("Part 2 = %d \n", litAfter(50))
}

func litAfter(times int) int {
    enhancer, puzzle := getData()
    for i := 0; i < times; i++ {
        puzzle = puzzle.enhance(enhancer)
    }
    return len(puzzle.grid)
}

func getData() (Enhancer, Graph) {
    data, _ := ioutil.ReadFile("data.txt")
    enhancerPuzzle := strings.Split(string(data), "\r\n\r\n")
    enhancer, puzzle := enhancerPuzzle[0], enhancerPuzzle[1]
    return Enhancer(enhancer), parsePuzzle(puzzle)
}

func parsePuzzle(raw string) Graph {
    graph := make(map[Position]bool)
    for y, line := range strings.Split(raw, "\r\n") {
        for x, value := range line {
            if value == '#' {
                graph[Position{x, y}] = true
            }
        }
    }
    return Graph{graph, 0}
}
