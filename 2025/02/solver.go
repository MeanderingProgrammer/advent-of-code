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
			length := longestPrefix(s)
			if length == (len(s)+1)/2 {
				part1 += i
			}
			if length > 0 {
				part2 += i
			}
		}
	}

	answer.Part1(23701357374, part1)
	answer.Part2(34284458938, part2)
}

func longestPrefix(s string) int {
	for i := len(s) / 2; i > 0; i-- {
		if isPrefix(s, i) {
			return i
		}
	}
	return 0
}

func isPrefix(s string, size int) bool {
	if len(s)%size != 0 {
		return false
	}
	prefix := s[0:size]
	for i := size; i < len(s); i += size {
		if prefix != s[i:i+size] {
			return false
		}
	}
	return true
}
