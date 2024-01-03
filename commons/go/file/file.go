package file

import (
	"advent-of-code/commons/go/util"
	"flag"
	"os"
	"runtime"
	"strings"
)

var testMode bool

func init() {
	flag.BoolVar(&testMode, "test", false, "Test mode")
	flag.Parse()
}

func ReadInt() []int {
	return Read(util.ToInt)
}

func Read[T any](f func(string) T) []T {
	var result []T
	for _, line := range ReadLines() {
		result = append(result, f(line))
	}
	return result
}

func ReadGroups() []string {
	return SplitContent("\n\n")
}

func ReadLines() []string {
	return SplitContent("\n")
}

func SplitContent(splitter string) []string {
	return strings.Split(Content(), splitter)
}

func Content() string {
	year, day := getYearDay()
	filepath := []string{"data", year, day, fileName()}
	content, err := os.ReadFile(strings.Join(filepath, "/"))
	util.CheckError(err)
	return strings.ReplaceAll(string(content), "\r\n", "\n")
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
	if testMode {
		return "sample.txt"
	} else {
		return "data.txt"
	}
}
