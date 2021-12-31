package files

import (
	"advent-of-code/commons/go/conversions"
	"advent-of-code/commons/go/utils"
	"io/ioutil"
	"strings"
)

// Read sample file rather than actual input
const test_mode = false

func ReadInt() []int {
	toInt := func(line string) interface{} {
		return conversions.ToInt(line)
	}
	var result []int
	for _, value := range Read(toInt) {
		result = append(result, value.(int))
	}
	return result
}

func Read(f func(string)interface{}) []interface{} {
	var result []interface{}
	for _, line := range ReadLines() {
		result = append(result, f(line))
	}
	return result
} 

func ReadLines() []string {
	content, err := ioutil.ReadFile(fileName())
	utils.CheckError(err)
	return strings.Split(string(content), "\r\n")
}

func fileName() string {
	if test_mode {
		return "sample.txt"
	} else {
		return "data.txt"
	}
}
