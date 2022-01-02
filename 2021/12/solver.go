package main

import(
    "advent-of-code/commons/go/answers"
    "advent-of-code/commons/go/files"
    "strings"
    "unicode"
)

type Cave string

func (cave Cave) isBig() bool {
    return unicode.IsUpper(rune(cave[0]))
}

type Path []Cave

func (path Path) add(cave Cave) Path {
    desination := make([]Cave, len(path))
    copy(desination, path)
    return append(desination, cave)
}

func (path Path) last() Cave {
    return path[len(path) - 1]
}

func (path Path) contains(destination Cave) bool {
    for _, cave := range path {
        if cave == destination {
            return true
        }
    }
    return false
}

func (path Path) containsLower() bool {
    lowerCounts := make(map[Cave]int)
    for _, cave := range path {
        if !cave.isBig() {
            lowerCounts[cave]++
            if lowerCounts[cave] > 1 {
                return true
            }
        }
    }
    return false
}

type Paths []Path

func (paths *Paths) pop() Path {
    value := (*paths)[0]
    *paths = (*paths)[1:]
    return value
}

func (paths *Paths) add(path Path) {
    *paths = append(*paths, path)
}

func (paths Paths) empty() bool {
    return len(paths) == 0
}

type Graph map[Cave][]Cave

func (graph Graph) add(start Cave, end Cave) {
    _, exists := graph[start]
    if exists {
        graph[start] = append(graph[start], end)
    } else {
        graph[start] = []Cave{end}
    }
}

func (graph Graph) paths(canGo func(Path, Cave) bool) Paths {
    var complete Paths
    inProgress := Paths([]Path{[]Cave{"start"}})

    for !inProgress.empty() {
        current := inProgress.pop()
        if current.last() == "end" {
            complete.add(current)
        } else {
            neighbors := graph[current.last()]
            for _, neighbor := range neighbors {
                if canGo(current, neighbor) {
                    inProgress.add(current.add(neighbor))
                }
            }
        }
    }

    return complete
}

func main() {
    graph := getGraph()

    answers.Part1(3497, len(graph.paths(part1)))
    answers.Part2(93686, len(graph.paths(part2)))
}

func part1(path Path, destination Cave) bool {
    if destination.isBig() {
        return true
    } else {
        return !path.contains(destination)
    }
}

func part2(path Path, destination Cave) bool {
    if destination.isBig() {
        return true
    } else if destination == "start" {
        return false
    } else if (!path.containsLower()) {
        return true
    } else {  
        return !path.contains(destination)
    }
}

func getGraph() Graph {
    graph := make(Graph)
    for _, creationRule := range files.ReadLines() {
        startEnd := strings.Split(creationRule, "-")
        start, end := Cave(startEnd[0]), Cave(startEnd[1])
        graph.add(start, end)
        graph.add(end, start)
    }
    return graph
}
