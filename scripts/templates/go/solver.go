package main

import (
	"advent-of-code/commons/go/answer"
	"advent-of-code/commons/go/file"
	"fmt"
)

func main() {
	data := file.ReadLines()
	fmt.Println(data)
	answer.Part1(1, 1)
}
