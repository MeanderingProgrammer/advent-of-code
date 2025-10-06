package main

import (
	"sort"

	"advent-of-code/commons/go/answer"
	"advent-of-code/commons/go/file"
	"advent-of-code/commons/go/util"
)

type Stack []rune

func (stack *Stack) push(value rune) {
	*stack = append(*stack, value)
}

func (stack *Stack) pop() rune {
	value := (*stack)[len(*stack)-1]
	*stack = (*stack)[:len(*stack)-1]
	return value
}

func (stack Stack) empty() bool {
	return len(stack) == 0
}

var closing = map[rune]rune{
	'(': ')',
	'[': ']',
	'{': '}',
	'<': '>',
}

type Score struct {
	mismatch   int
	incomplete int
}

var scores = map[rune]Score{
	')': {3, 1},
	']': {57, 2},
	'}': {1197, 3},
	'>': {25137, 4},
}

type System string

func (system System) check() (rune, Stack) {
	var stack Stack
	for _, brace := range system {
		_, exists := closing[brace]
		if exists {
			stack.push(brace)
		} else {
			open := stack.pop()
			if brace != closing[open] {
				return brace, nil
			}
		}
	}
	return '0', stack
}

type Systems []string

func (systems Systems) mismatch() int {
	values := util.Map(systems, func(system string) int {
		brace, _ := System(system).check()
		return scores[brace].mismatch
	})
	return util.Sum(values)
}

func (systems Systems) autocomplete() int {
	values := util.Map(systems, func(system string) int {
		_, remainder := System(system).check()
		score := 0
		for !remainder.empty() {
			brace := closing[remainder.pop()]
			score = score*5 + scores[brace].incomplete
		}
		return score
	})

	results := util.Filter(values, func(value int) bool {
		return value > 0
	})

	sort.Ints(results)
	return results[len(results)/2]
}

func main() {
	answer.Timer(solution)
}

func solution() {
	systems := Systems(file.Default[string]().ReadLines())
	answer.Part1(321237, systems.mismatch())
	answer.Part2(2360030859, systems.autocomplete())
}
