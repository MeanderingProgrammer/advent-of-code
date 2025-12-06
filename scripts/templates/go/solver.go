package main

import (
	"fmt"

	"advent-of-code/lib/go/answer"
	"advent-of-code/lib/go/file"
)

func main() {
	answer.Timer(solution)
}

func solution() {
	data := file.Default().Lines()
	fmt.Println(data)
	answer.Part1(1, 1)
	answer.Part2(1, 1)
}
