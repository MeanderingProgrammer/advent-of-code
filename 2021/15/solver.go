package main

import (
	"advent-of-code/commons/go/answers"
	"advent-of-code/commons/go/conversions"
	"advent-of-code/commons/go/files"
	"advent-of-code/commons/go/parsers"
)

type Path struct {
	path  []parsers.Point
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
			minIndex, minPath = i+1, path
		}
	}
	*priorityQueue = append((*priorityQueue)[:minIndex], (*priorityQueue)[minIndex+1:]...)
	return minPath
}

func main() {
	answers.Part1(656, solve(getGrid(false)))
	answers.Part2(2979, solve(getGrid(true)))
}

func solve(grid parsers.Grid) int {
	end := parsers.Point{
		X: grid.Width,
		Y: grid.Height,
	}

	var priorityQueue PriorityQueue
	priorityQueue.add(Path{
		path:  []parsers.Point{{X: 0, Y: 0}},
		value: 0,
	})

	seen := make(map[parsers.Point]bool)

	for !priorityQueue.empty() {
		path := priorityQueue.pop()
		lastPoint := path.path[len(path.path)-1]
		if lastPoint == end {
			return path.value
		}
		for _, neighbor := range lastPoint.Adjacent(false) {
			value, exists := grid.Get(neighbor), grid.Contains(neighbor)
			if exists && !seen[neighbor] {
				seen[neighbor] = true
				priorityQueue.add(path.add(neighbor, conversions.ToInt(value)))
			}
		}
	}

	return 0
}

func getGrid(wrap bool) parsers.Grid {
	grid := baseGrid()
	if wrap {
		points, baseSize := grid.Points(), grid.Width+1
		for i := 0; i < 5; i++ {
			for j := 0; j < 5; j++ {
				distance := i + j
				if distance == 0 {
					continue
				}
				for _, point := range points {
					newPoint := parsers.Point{
						X: point.X + (baseSize * i),
						Y: point.Y + (baseSize * j),
					}
					newValue := conversions.ToInt(grid.Get(point)) + distance
					if newValue > 9 {
						newValue -= 9
					}
					grid.Set(newPoint, conversions.ToString(newValue))
				}
			}
		}
	}
	return grid
}

func baseGrid() parsers.Grid {
	return parsers.ConstructGrid(files.ReadLines(), parsers.Character, "")
}
