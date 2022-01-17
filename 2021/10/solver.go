package main

import (
	"advent-of-code/commons/go/answers"
	"advent-of-code/commons/go/files"
	"advent-of-code/commons/go/utils"
	"sort"
)

type Stack []string

func (stack *Stack) push(value string) {
	*stack = append(*stack, value)
}

func (stack *Stack) pop() string {
	value := (*stack)[len(*stack)-1]
	*stack = (*stack)[:len(*stack)-1]
	return value
}

func (stack Stack) empty() bool {
	return len(stack) == 0
}

var openToClose = map[string]string{
	"(": ")",
	"[": "]",
	"{": "}",
	"<": ">",
}

type Score struct {
	mismatch   int
	incomplete int
}

var scores = map[string]Score{
	")": {3, 1},
	"]": {57, 2},
	"}": {1197, 3},
	">": {25137, 4},
}

type System string

func (system System) checkSyntax() (string, Stack) {
	var syntaxStack Stack
	for _, raw := range system {
		value := string(raw)
		_, exists := openToClose[value]
		if exists {
			syntaxStack.push(value)
		} else {
			lastOpen := syntaxStack.pop()
			matchingClose := openToClose[lastOpen]
			if matchingClose != value {
				return value, nil
			}
		}
	}
	return "", syntaxStack
}

type Systems []string

func (systems Systems) mismatchScore() int {
	toMimatchScore := func(system string) int {
		mismatched, _ := System(system).checkSyntax()
		return scores[mismatched].mismatch
	}
	return utils.Sum(utils.Map(systems, toMimatchScore))
}

func (systems Systems) autocompleteScore() int {
	toAutocompleteScore := func(system string) int {
		_, unmatched := System(system).checkSyntax()
		incompleteScore := 0
		for !unmatched.empty() {
			unmatchedBrace := unmatched.pop()
			neededBrace := openToClose[unmatchedBrace]
			incompleteScore *= 5
			incompleteScore += scores[neededBrace].incomplete
		}
		return incompleteScore
	}

	nonZero := func(value int) bool {
		return value > 0
	}

	scores := utils.Filter(
		utils.Map(systems, toAutocompleteScore),
		nonZero,
	)

	sort.Ints(scores)
	return scores[len(scores)/2]
}

func main() {
	systems := getSystem()

	answers.Part1(321237, systems.mismatchScore())
	answers.Part2(2360030859, systems.autocompleteScore())
}

func getSystem() Systems {
	return files.ReadLines()
}
