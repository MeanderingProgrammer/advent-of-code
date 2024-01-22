package main

import (
	"advent-of-code/commons/go/answer"
	"advent-of-code/commons/go/file"
	"fmt"
)

func main() {
	answer.Timer(solution)
}

func solution() {
	data := file.Default[string]().ReadLines()
	fmt.Println(data)
	answer.Part1(1, 1)
}
