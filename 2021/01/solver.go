package main

import(
    "advent-of-code/commons/go/answers"
    "advent-of-code/commons/go/files"
)

func main() {
    content := files.ReadInt()

    answers.Part1(1292, windowIncreases(content, 1))
    answers.Part2(1262, windowIncreases(content, 3))
}

func windowIncreases(content []int, windowSize int) int {
    increases := 0
    for i := range content[:len(content) - windowSize] {
        if (sum(content, windowSize, i+1) > sum(content, windowSize, i)) {
            increases++
        }
    }
    return increases
}

func sum(values []int, windowSize int, start int) int {
    result := 0
    for _, value := range values[start:start+windowSize] {
        result += value
    }
    return result
}
