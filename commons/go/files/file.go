package files

import (
	"advent-of-code/commons/go/conversions"
	"advent-of-code/commons/go/utils"
	"os"
	"strings"
)

// Read sample file rather than actual input
const test_mode = false

func ReadInt() []int {
	toInt := func(line string) int {
		return conversions.ToInt(line)
	}
	return Read(toInt)
}

func Read[T any](f func(string) T) []T {
	var result []T
	for _, line := range ReadLines() {
		result = append(result, f(line))
	}
	return result
}

func ReadGroups() []string {
	return SplitContent("\r\n\r\n")
}

func ReadLines() []string {
	return SplitContent("\r\n")
}

func SplitContent(splitter string) []string {
	return strings.Split(Content(), splitter)
}

func Content() string {
	content, err := os.ReadFile(fileName())
	utils.CheckError(err)
	return string(content)
}

func fileName() string {
	if test_mode {
		return "sample.txt"
	} else {
		return "data.txt"
	}
}
