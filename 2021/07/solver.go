package main

import (
	"advent-of-code/commons/go/answers"
	"advent-of-code/commons/go/files"
	"advent-of-code/commons/go/parsers"
	"advent-of-code/commons/go/utils"
	"sort"
)

type Positions []int

func (positions Positions) minimize(f func(int) int) int {
	start, end := positions[0], positions[len(positions)-1]
	minimum := positions.cost(f, start)
	for i := start + 1; i <= end; i++ {
		value := positions.cost(f, i)
		minimum = utils.Min(minimum, value)
	}
	return minimum
}

func (positions Positions) cost(f func(int) int, targetPosition int) int {
	cost := 0
	for _, position := range positions {
		distance := utils.Abs(position - targetPosition)
		cost += f(distance)
	}
	return cost
}

func main() {
	positions := getPositions()

	answers.Part1(352331, positions.minimize(linear))
	answers.Part2(99266250, positions.minimize(exponential))
}

func linear(distance int) int {
	return distance
}

func exponential(distance int) int {
	return ((distance * distance) + distance) / 2
}

func getPositions() Positions {
	positions := parsers.IntCsv(files.Content())
	sort.Ints(positions)
	return positions
}
