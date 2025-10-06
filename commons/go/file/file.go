package file

import (
	"flag"
	"os"
	"runtime"
	"strings"

	"advent-of-code/commons/go/util"
)

type Reader[T any] struct {
	path string
}

func New[T any](path string) Reader[T] {
	return Reader[T]{path}
}

func Default[T any]() Reader[T] {
	var testMode bool
	flag.BoolVar(&testMode, "test", false, "Test mode")
	flag.Parse()
	year, day := getYearDay()
	filepath := []string{"data", year, day, fileName(testMode)}
	return New[T](strings.Join(filepath, "/"))
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

func fileName(testMode bool) string {
	if testMode {
		return "sample.txt"
	} else {
		return "data.txt"
	}
}

func (r Reader[T]) Read(f func(string) T) []T {
	var result []T
	for _, line := range r.ReadLines() {
		result = append(result, f(line))
	}
	return result
}

func (r Reader[T]) ReadGroups() []string {
	return r.SplitContent("\n\n")
}

func (r Reader[T]) ReadLines() []string {
	return r.SplitContent("\n")
}

func (r Reader[T]) SplitContent(splitter string) []string {
	return strings.Split(r.Content(), splitter)
}

func (r Reader[T]) Content() string {
	content := util.Must1(os.ReadFile(r.path))
	return strings.ReplaceAll(string(content), "\r\n", "\n")
}
