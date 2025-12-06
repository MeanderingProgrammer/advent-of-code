package main

import (
	"advent-of-code/lib/go/answer"
	"advent-of-code/lib/go/file"
	"advent-of-code/lib/go/util"
)

func main() {
	answer.Timer(solution)
}

func solution() {
	lines := file.Default().Lines()
	values := util.Map(lines, util.ToInt)
	answer.Part1(1292, increases(values, 1))
	answer.Part2(1262, increases(values, 3))
}

func increases(values []int, n int) int {
	result := 0
	for i := range values[:len(values)-n] {
		if sum(values, n, i+1) > sum(values, n, i) {
			result++
		}
	}
	return result
}

func sum(values []int, n int, start int) int {
	result := 0
	for _, value := range values[start : start+n] {
		result += value
	}
	return result
}
