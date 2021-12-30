package answers

import "fmt"

func Part1(expected, result int) {
	part(1, expected, result)
}

func Part2(expected, result int) {
	part(2, expected, result)
}

func part(part, expected, result int) {
	if expected != result {
		panic(fmt.Sprintf("Part %d incorrect, expected %d but got %d", part, expected, result))
	}
	fmt.Println(fmt.Sprintf("Part %d: %d", part, result))
}
