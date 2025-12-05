package main

import (
	"strings"
	"sync"

	"advent-of-code/commons/go/answer"
	"advent-of-code/commons/go/file"
	"advent-of-code/commons/go/util"
)

type Response struct {
	value int
	parts int
}

func main() {
	answer.Timer(solution)
}

func solution() {
	values := file.Default().Split(",")

	out := make(chan Response)
	var wg sync.WaitGroup
	for _, value := range values {
		wg.Go(func() {
			ids := util.Map(strings.Split(value, "-"), util.ToInt)
			for i := ids[0]; i <= ids[1]; i++ {
				s := util.ToString(i)
				length := longestPrefix(s)
				if length > 0 {
					out <- Response{value: i, parts: len(s) / length}
				}
			}
		})
	}
	go func() {
		wg.Wait()
		close(out)
	}()

	part1 := 0
	part2 := 0
	for response := range out {
		if response.parts == 2 {
			part1 += response.value
		}
		part2 += response.value
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
