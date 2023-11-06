package main

import (
	"advent-of-code/commons/go/answers"
	"advent-of-code/commons/go/files"
)

func main() {
	values := files.ReadInt()
	answers.Part1(1292, windowIncreases(values, 1))
	answers.Part2(1262, windowIncreases(values, 3))
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
