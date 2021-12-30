package main

import (
	"fmt"
	"io/ioutil"
	"sort"
	"strings"
)

type Stack []string

func (stack *Stack) push(value string) {
    *stack = append(*stack, value)
}

func (stack *Stack) pop() string {
    value := (*stack)[len(*stack) - 1]
    *stack = (*stack)[:len(*stack) - 1]
    return value
}

func (stack Stack) empty() bool {
    return len(stack) == 0
}

var openToClose = map[string]string {
    "(": ")",
    "[": "]",
    "{": "}",
    "<": ">",
}

type Score struct {
    mismatch int
    incomplete int
}

var scores = map[string]Score {
    ")": {3, 1},
    "]": {57, 2},
    "}": {1197, 3},
    ">": {25137, 4},
}

type Systems []string

func (systems Systems) mismatchScore() int {
    total := 0
    for _, system := range systems {
        mismatched, _ := checkSyntax(system)
        score := scores[mismatched].mismatch
        total += score
    }
    return total
}

func (systems Systems) autocompleteScore() int {
    var totals []int
    for _, system := range systems {
        _, unmatched := checkSyntax(system)
        incompleteScore := 0
        for !unmatched.empty() {
            unmatchedBrace := unmatched.pop()
            neededBrace := openToClose[unmatchedBrace]
            incompleteScore *= 5
            incompleteScore += scores[neededBrace].incomplete
        }
        if incompleteScore > 0 {
            totals = append(totals, incompleteScore)
        }
    }
    sort.Ints(totals)
    return totals[len(totals) / 2]
}

func main() {
    systems := getData()

    // Part 1: 321237
    fmt.Printf("Part 1: %d \n", systems.mismatchScore())
    // Part 2: 2360030859
    fmt.Printf("Part 2: %d \n", systems.autocompleteScore())
}

func checkSyntax(system string) (string, Stack) {
    var syntaxStack Stack
    for _, raw := range system {
        value := string(raw)
        _, exists := openToClose[value]
        if exists {
            syntaxStack.push(value)
        } else {
            lastOpen := syntaxStack.pop()
            matchingClose, _ := openToClose[lastOpen]
            if matchingClose != value {
                return value, nil
            }
        }
    }
    return "", syntaxStack
}
    

func getData() Systems {
    data, _ := ioutil.ReadFile("data.txt")
    return strings.Split(string(data), "\r\n")
}
