package main

import (
	"advent-of-code/commons/go/answer"
	"advent-of-code/commons/go/file"
	"advent-of-code/commons/go/graph"
	"advent-of-code/commons/go/util"
	"hash/fnv"
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

func (path Path) Hash() uint64 {
	h := fnv.New64()
	for _, cave := range path {
		h.Write([]byte(cave))
	}
	return h.Sum64()
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
	answer.Timer(solution)
}

func solution() {
	graph := getGraph()
	answer.Part1(3497, paths(graph, part1))
	answer.Part2(93686, paths(graph, part2))
}

func getGraph() graph.Graph[Cave, string] {
	var pairs [][2]Cave
	for _, creationRule := range file.Default[string]().ReadLines() {
		startEnd := strings.Split(creationRule, "-")
		pair := [2]Cave{Cave(startEnd[0]), Cave(startEnd[1])}
		pairs = append(pairs, pair)
	}
	return graph.ConstructDirectly(pairs)
}

func paths(g graph.Graph[Cave, string], canGo func(Path, Cave) bool) int {
	result := graph.Search[Path]{
		Initial: Path([]Cave{"start"}),
		Done: func(state Path) bool {
			return state.last() == "end"
		},
		NextStates: func(state Path) []Path {
			nextStates := []Path{}
			for _, neighbor := range g.Neighbors(state.last()) {
				if canGo(state, neighbor) {
					nextStates = append(nextStates, state.add(neighbor))
				}
			}
			return nextStates
		},
		FirstOnly: false,
	}.Dijkstra()
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
