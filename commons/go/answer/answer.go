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

func Part1[T comparable](expected, actual T) {
	part(1, expected, actual)
}

func Part2[T comparable](expected, actual T) {
	part(2, expected, actual)
}

func part[T comparable](part int, expected T, actual T) {
	if expected != actual {
		panic(fmt.Sprintf("Part %d incorrect, expected %v but got %v", part, expected, actual))
	}
	fmt.Println(fmt.Sprintf("Part %d: %v", part, actual))
}
