package main

import (
	"advent-of-code/commons/go/answers"
	"advent-of-code/commons/go/files"
	"fmt"
)

func main() {
	data := files.ReadLines()
	fmt.Println(data)
	answers.Part1(1, 1)
}
