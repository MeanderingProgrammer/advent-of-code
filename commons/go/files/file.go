package files

import (
	"io/ioutil"
	"strconv"
	"strings"
)

// Read sample file rather than actual input
const test_mode = false

func ReadInt() []int {
	var result []int
	for _, stringValue := range Read() {
		value, err := strconv.Atoi(stringValue)
		checkError(err)
		result = append(result, value)
	}
	return result
}

func Read() []string {
	content, err := ioutil.ReadFile(fileName())
	checkError(err)
	return strings.Split(string(content), "\r\n")
}

func fileName() string {
	if test_mode {
		return "sample.txt"
	} else {
		return "data.txt"
	}
}

func checkError(err error) {
	if err != nil {
		panic(err)
	}
}
