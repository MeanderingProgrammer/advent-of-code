package main

import (
	"advent-of-code/commons/go/answers"
	"advent-of-code/commons/go/conversions"
	"advent-of-code/commons/go/files"
	"advent-of-code/commons/go/parsers"
	"sort"
)

type Points []parsers.Point

func (points Points) contains(point parsers.Point) bool {
    for _, contained := range points {
        if contained == point {
            return true
        }
    }
    return false
}

func (points Points) riskLevel(graph parsers.Graph) int {
    result := 0
    for _, point := range points {        
        result += conversions.ToInt(graph.Grid[point]) + 1
    }
    return result
}

func (points Points) basinSizes(graph parsers.Graph) []int {
    var basinSizes []int
    for _, point := range points {
        basinSizes = append(basinSizes, basinSize(graph, point))
    }
    return basinSizes
}

func basinSize(graph parsers.Graph, point parsers.Point) int {
    basin := Points{point}
    for i := 0; i < len(basin); i++ {
        for _, adjacent := range basin[i].Adjacent(false) {
            adjacentValue, exists := graph.Grid[adjacent]
            if exists && conversions.ToInt(adjacentValue) < 9 && !basin.contains(adjacent) {
                basin = append(basin, adjacent)
            }
        }
    }
    return len(basin)
}

func main() {
    graph := getGraph()

    minimums := minimums(graph)
    answers.Part1(506, minimums.riskLevel(graph))

    basinSizes := minimums.basinSizes(graph)
    sort.Sort(sort.Reverse(sort.IntSlice(basinSizes)))
    answers.Part2(931200, basinSizes[0] * basinSizes[1] * basinSizes[2])
}

func minimums(graph parsers.Graph) Points {
    var result Points
    for point := range graph.Grid {
        if isMinimum(graph, point) {
            result = append(result, point)
        }
    }
    return result
}

func isMinimum(graph parsers.Graph, point parsers.Point) bool {
    value := conversions.ToInt(graph.Grid[point])
    for _, adjacent := range point.Adjacent(false) {
        adjacentValue, exists := graph.Grid[adjacent]
        if exists && conversions.ToInt(adjacentValue) <= value {
            return false
        }
    }
    return true
}

func getGraph() parsers.Graph {
    return parsers.ConstructGraph(files.Content(), parsers.Character, "")
}
