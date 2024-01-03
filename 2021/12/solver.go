package main

import (
	"advent-of-code/commons/go/answer"
	"advent-of-code/commons/go/file"
	"advent-of-code/commons/go/graph"
	"advent-of-code/commons/go/queue"
	"advent-of-code/commons/go/util"
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

func (path Path) ToString() string {
	return fmt.Sprintf("%v", path)
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
	return util.Contains(path, destination)
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
	answer.Part1(3497, paths(graph, part1))
	answer.Part2(93686, paths(graph, part2))
}

func getGraph() graph.Graph[Cave, string] {
	var pairs [][2]Cave
	for _, creationRule := range file.ReadLines() {
		startEnd := strings.Split(creationRule, "-")
		pair := [2]Cave{Cave(startEnd[0]), Cave(startEnd[1])}
		pairs = append(pairs, pair)
	}
	return graph.ConstructDirectly(pairs)
}

func paths(g graph.Graph[Cave, string], canGo func(Path, Cave) bool) int {
	result := g.Bfs(graph.Search{
		Initial: Path([]Cave{"start"}),
		Done: func(state queue.State) bool {
			return state.(Path).last() == "end"
		},
		NextStates: func(state queue.State) []queue.State {
			nextStates := []queue.State{}
			for _, neighbor := range g.Neighbors(state.(Path).last()) {
				if canGo(state.(Path), neighbor) {
					nextStates = append(nextStates, state.(Path).add(neighbor))
				}
			}
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
