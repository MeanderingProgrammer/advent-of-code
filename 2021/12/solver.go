package main

import (
	"advent-of-code/commons/go/answers"
	"advent-of-code/commons/go/files"
	"advent-of-code/commons/go/graphs"
	"advent-of-code/commons/go/utils"
	"fmt"
	"strings"
	"unicode"
)

type Cave string

func (cave Cave) isBig() bool {
	return unicode.IsUpper(rune(cave[0]))
}

type Path []Cave

func (path Path) Cost() int {
	return len(path)
}

func (path Path) String() *string {
	result := fmt.Sprintf("%v", path)
	return &result
}

func (path Path) last() Cave {
	return path[len(path)-1]
}

func (path Path) add(cave Cave) Path {
	desination := make([]Cave, len(path))
	copy(desination, path)
	return append(desination, cave)
}

func (path Path) contains(destination Cave) bool {
	return utils.Contains(path, destination)
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

func main() {
	graph := getGraph()
	answers.Part1(3497, paths(graph, part1))
	answers.Part2(93686, paths(graph, part2))
}

func getGraph() graphs.Graph[Cave, string] {
	var pairs [][2]Cave
	for _, creationRule := range files.ReadLines() {
		startEnd := strings.Split(creationRule, "-")
		pair := [2]Cave{Cave(startEnd[0]), Cave(startEnd[1])}
		pairs = append(pairs, pair)
	}
	return graphs.ConstructDirectly(pairs)
}

func paths(graph graphs.Graph[Cave, string], canGo func(Path, Cave) bool) int {
	result := graph.Bfs(graphs.Search{
		Initial: Path([]Cave{"start"}),
		Done: func(state graphs.State) bool {
			return state.(Path).last() == "end"
		},
		NextStates: func(state graphs.State) <-chan graphs.State {
			var neighbors []Cave
			for _, neighbor := range graph.Neighbors(state.(Path).last()) {
				if canGo(state.(Path), neighbor) {
					neighbors = append(neighbors, neighbor)
				}
			}
			nextStates := make(chan graphs.State, len(neighbors))
			for _, neighbor := range neighbors {
				nextStates <- state.(Path).add(neighbor)
			}
			close(nextStates)
			return nextStates
		},
		FirstOnly: false,
	})
	return len(result.Completed)
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
	} else if !path.containsLower() {
		return true
	} else {
		return !path.contains(destination)
	}
}
