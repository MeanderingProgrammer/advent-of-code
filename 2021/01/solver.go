package main

import (
	"advent-of-code/commons/go/answer"
	"advent-of-code/commons/go/file"
)

func main() {
	answer.Timer(solution)
}

func solution() {
	values := file.ReadInt()
	answer.Part1(1292, windowIncreases(values, 1))
	answer.Part2(1262, windowIncreases(values, 3))
}

func windowIncreases(values []int, windowSize int) int {
	increases := 0
	for i := range values[:len(values)-windowSize] {
		if sum(values, windowSize, i+1) > sum(values, windowSize, i) {
			increases++
		}
	}
	return increases
}

func sum(values []int, windowSize int, start int) int {
	result := 0
	for _, value := range values[start : start+windowSize] {
		result += value
	}
	return result
}
