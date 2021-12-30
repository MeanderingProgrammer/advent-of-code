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

func (position Position) adjacent() []Position {
    return []Position{
        {position.x - 1, position.y},
        {position.x + 1, position.y},
        {position.x, position.y - 1},
        {position.x, position.y + 1},
    }
}

type Path struct {
    path []Position
    value int
}

func (path Path) add(position Position, value int) Path {
    newPositions := make([]Position, len(path.path))
    copy(newPositions, path.path)
    return Path{append(newPositions, position), path.value + value}
}

type PriorityQueue []Path

func (priorityQueue *PriorityQueue) add(path Path) {
    *priorityQueue = append(*priorityQueue, path)
}

func (priorityQueue PriorityQueue) empty() bool {
    return len(priorityQueue) == 0
}

func (priorityQueue *PriorityQueue) pop() Path {
    minIndex, minPath := 0, (*priorityQueue)[0]
    for i, path := range (*priorityQueue)[1:] {
        if path.value < minPath.value {
            minIndex, minPath = i + 1, path
        }
    }
    *priorityQueue = append((*priorityQueue)[:minIndex], (*priorityQueue)[minIndex + 1:]...)
    return minPath
}

type Graph struct {
    graph map[Position]int
    end int
}

func (graph Graph) solve() int {
    end := Position{graph.end, graph.end}

    var priorityQueue PriorityQueue
    priorityQueue.add(Path{[]Position{{0, 0}}, 0})

    seen := make(map[Position]bool)

    for !priorityQueue.empty() {
        path := priorityQueue.pop()
        lastPosition := path.path[len(path.path) - 1]
        if lastPosition == end {
            return path.value
        }
        for _, neighbor := range lastPosition.adjacent() {
            value, exists := graph.graph[neighbor]
            if exists && !seen[neighbor] {
                seen[neighbor] = true
                priorityQueue.add(path.add(neighbor, value))
            }
        }
    }

    return 0
}

func (graph Graph) print() {
    for y := 0; y < graph.end; y++ {
        for x := 0; x < graph.end; x++ {
            position := Position{x, y}
            fmt.Print(graph.graph[position])
        }
        fmt.Println()
    }
}

func main() {
    // Part 1: 656
    fmt.Printf("Part 1: %d \n", getData(false).solve())
    // Part 2: 2979
    fmt.Printf("Part 2: %d \n", getData(true).solve())
}

func getData(wrap bool) Graph {
    baseGraph := baseData()
    if !wrap {
        return baseGraph
    } else {
        baseSize := baseGraph.end + 1
        graph := make(map[Position]int)
        for i := 0; i < 5; i++ {
            for j := 0; j < 5; j++ {
                distance := i + j
                for position, value := range baseGraph.graph {
                    newPosition := Position{position.x + (baseSize * i), position.y + (baseSize * j)}
                    newValue := value + distance
                    if newValue > 9 {
                        newValue -= 9
                    }
                    graph[newPosition] = newValue
                }
            }
        }
        return Graph{graph, (baseSize * 5) - 1}
    }
}

func baseData() Graph {
    data, _ := ioutil.ReadFile("data.txt")
    rows := strings.Split(string(data), "\r\n")
    graph := make(map[Position]int)
    for y, row := range rows {
        for x, rawValue := range(row) {
            position := Position{x, y}
            value := rawValue - '0'
            graph[position] = int(value)
        }
    }
    return Graph{graph, len(rows) - 1}
}
