package main

import (
	"advent-of-code/commons/go/answers"
    "advent-of-code/commons/go/conversions"
	"advent-of-code/commons/go/files"
	"advent-of-code/commons/go/parsers"
)

type Path struct {
    path []parsers.Point
    value int
}

func (path Path) add(point parsers.Point, value int) Path {
    newPoints := make([]parsers.Point, len(path.path))
    copy(newPoints, path.path)
    return Path{append(newPoints, point), path.value + value}
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

func main() {
    answers.Part1(656, solve(getGraph(false)))
    answers.Part2(2979, solve(getGraph(true)))
}

func solve(graph parsers.Graph) int {
    end := parsers.Point{
        X: graph.Width, 
        Y: graph.Height,
    }

    var priorityQueue PriorityQueue
    priorityQueue.add(Path{
        path: []parsers.Point{{X: 0, Y: 0}}, 
        value: 0,
    })

    seen := make(map[parsers.Point]bool)

    for !priorityQueue.empty() {
        path := priorityQueue.pop()
        lastPoint := path.path[len(path.path) - 1]
        if lastPoint == end {
            return path.value
        }
        for _, neighbor := range lastPoint.Adjacent(false) {
            value, exists := graph.Grid[neighbor]
            if exists && !seen[neighbor] {
                seen[neighbor] = true
                priorityQueue.add(path.add(neighbor, conversions.ToInt(value)))
            }
        }
    }

    return 0
}

func getGraph(wrap bool) parsers.Graph {
    baseGraph := baseGraph()
    if !wrap {
        return baseGraph
    } else {
        baseSize := baseGraph.Width + 1
        graph := make(map[parsers.Point]string)
        for i := 0; i < 5; i++ {
            for j := 0; j < 5; j++ {
                distance := i + j
                for point, value := range baseGraph.Grid {
                    newPoint := parsers.Point{
                        X: point.X + (baseSize * i), 
                        Y: point.Y + (baseSize * j),
                    }
                    newValue := conversions.ToInt(value) + distance
                    if newValue > 9 {
                        newValue -= 9
                    }
                    graph[newPoint] = conversions.ToString(newValue)
                }
            }
        }
        return parsers.Graph{
            Grid: graph, 
            Height: (baseSize * 5) - 1,
            Width: (baseSize * 5) - 1,
        }
    }
}

func baseGraph() parsers.Graph {
    return parsers.ConstructGraph(files.Content(), parsers.Character, "")
}
