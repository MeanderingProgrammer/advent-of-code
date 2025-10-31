package main

import (
	"fmt"

	"advent-of-code/commons/go/answer"
	"advent-of-code/commons/go/file"
)

func main() {
	answer.Timer(solution)
}

func solution() {
	data := file.Default[string]().ReadLines()
	fmt.Println(data)
	answer.Part1(1, 1)
	answer.Part2(1, 1)
}
