package main

import (
	"strings"

	"advent-of-code/commons/go/answer"
	"advent-of-code/commons/go/file"
	"advent-of-code/commons/go/util"
)

func main() {
	answer.Timer(solution)
}

func solution() {
	values := file.Default().Split(",")

	part1 := 0
	part2 := 0
	for _, value := range values {
		ids := util.Map(strings.Split(value, "-"), util.ToInt)
		for i := ids[0]; i <= ids[1]; i++ {
			s := util.ToString(i)
			if invalid(s, 2) {
				part1 += i
			}
			if anyInvalid(s) {
				part2 += i
			}
		}
	}

	answer.Part1(23701357374, part1)
	answer.Part2(34284458938, part2)
}

func anyInvalid(s string) bool {
	for i := 2; i <= len(s); i++ {
		if invalid(s, i) {
			return true
		}
	}
	return false
}

func invalid(s string, parts int) bool {
	if len(s)%parts != 0 {
		return false
	}
	size := len(s) / parts
	first := s[0:size]
	for i := size; i < len(s); i += size {
		part := s[i : i+size]
		if first != part {
			return false
		}
	}
	return true
}
