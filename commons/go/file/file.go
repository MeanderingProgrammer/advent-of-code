package file

import (
	"flag"
	"os"
	"runtime"
	"strings"

	"advent-of-code/commons/go/util"
)

type Reader struct {
	path string
}

func New(path string) Reader {
	return Reader{path}
}

func Default() Reader {
	var testMode bool
	flag.BoolVar(&testMode, "test", false, "Test mode")
	flag.Parse()
	year, day := getYearDay()
	filepath := []string{"data", year, day, fileName(testMode)}
	return New(strings.Join(filepath, "/"))
}

func getYearDay() (string, string) {
	i := 0
	for {
		_, file, _, _ := runtime.Caller(i)
		if strings.HasSuffix(file, "solver.go") {
			parts := strings.Split(file, "/")
			return parts[len(parts)-3], parts[len(parts)-2]
		}
		i++
	}
}

func fileName(testMode bool) string {
	if testMode {
		return "sample.txt"
	} else {
		return "data.txt"
	}
}

func (r Reader) Groups() []string {
	return r.Split("\n\n")
}

func (r Reader) Lines() []string {
	return r.Split("\n")
}

func (r Reader) Split(sep string) []string {
	return strings.Split(r.Content(), sep)
}

func (r Reader) Content() string {
	content := util.Must1(os.ReadFile(r.path))
	result := strings.ReplaceAll(string(content), "\r\n", "\n")
	return strings.TrimSuffix(result, "\n")
}
