package files

import (
	"advent-of-code/commons/go/conversions"
	"advent-of-code/commons/go/utils"
	"flag"
	"os"
	"runtime"
	"strings"
)

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
	return SplitContent("\n\n")
}

func ReadLines() []string {
	return SplitContent("\n")
}

func SplitContent(splitter string) []string {
	content := strings.ReplaceAll(Content(), "\r\n", "\n")
	return strings.Split(content, splitter)
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
	testMode := flag.Bool("test", false, "Test mode")
	flag.Parse()
	if *testMode {
		return "sample.txt"
	} else {
		return "data.txt"
	}
}
