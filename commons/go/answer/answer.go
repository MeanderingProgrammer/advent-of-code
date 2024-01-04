package answer

import (
	"fmt"
	"time"
)

func Timer(solution func()) {
	start := time.Now().UnixNano()
	solution()
	end := time.Now().UnixNano()
	fmt.Println(fmt.Sprintf("Runtime (ns): %d", end-start))
}

func Part1[T comparable](expected, result T) {
	part(1, expected, result)
}

func Part2[T comparable](expected, result T) {
	part(2, expected, result)
}

func part[T comparable](part int, expected T, result T) {
	if expected != result {
		panic(fmt.Sprintf("Part %d incorrect, expected %v but got %v", part, expected, result))
	}
	fmt.Println(fmt.Sprintf("Part %d: %v", part, result))
}
