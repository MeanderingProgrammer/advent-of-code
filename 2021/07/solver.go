package main

import (
	"sort"

	"advent-of-code/commons/go/answer"
	"advent-of-code/commons/go/file"
	"advent-of-code/commons/go/util"
)

type Positions []int

func (positions Positions) minimize(f func(int) int) int {
	start, end := positions[0], positions[len(positions)-1]
	minimum := positions.cost(f, start)
	for i := start + 1; i <= end; i++ {
		value := positions.cost(f, i)
		minimum = min(minimum, value)
	}
	return minimum
}

func (positions Positions) cost(f func(int) int, targetPosition int) int {
	cost := 0
	for _, position := range positions {
		distance := util.Abs(position - targetPosition)
		cost += f(distance)
	}
	return cost
}

func main() {
	answer.Timer(solution)
}

func solution() {
	positions := getPositions()
	answer.Part1(352331, positions.minimize(linear))
	answer.Part2(99266250, positions.minimize(exponential))
}

func linear(distance int) int {
	return distance
}

func exponential(distance int) int {
	return ((distance * distance) + distance) / 2
}

func getPositions() Positions {
	positions := util.IntCsv(file.Default[string]().Content())
	sort.Ints(positions)
	return positions
}
