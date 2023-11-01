package files

import (
	"advent-of-code/commons/go/conversions"
	"advent-of-code/commons/go/utils"
	"os"
	"runtime"
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
	year, day := getYearDay()
	filepath := []string{year, day, fileName()}
	content, err := os.ReadFile(strings.Join(filepath, "/"))
	utils.CheckError(err)
	return string(content)
}

func getYearDay() (string, string) {
	i := 0
	for true {
		_, file, _, _ := runtime.Caller(i)
		if strings.HasSuffix(file, "solver.go") {
			parts := strings.Split(file, "/")
			return parts[len(parts)-3], parts[len(parts)-2]
		}
		i++
	}
	return "", ""
}

func fileName() string {
	if test_mode {
		return "sample.txt"
	} else {
		return "data.txt"
	}
}
