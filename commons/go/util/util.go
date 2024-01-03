package util

import (
	"strconv"
	"strings"
)

func CheckError(err error) {
	if err != nil {
		panic(err)
	}
}

func Abs(value int) int {
	result := value
	if value < 0 {
		return result * -1
	}
	return result
}

func Max(v1, v2 int) int {
	result := v1
	if v2 > v1 {
		result = v2
	}
	return result
}

func Min(v1, v2 int) int {
	result := v1
	if v2 < v1 {
		result = v2
	}
	return result
}

func ToInt(value string) int {
	result, err := strconv.Atoi(value)
	CheckError(err)
	return result
}

func ToString(value int) string {
	return strconv.Itoa(value)
}

func BinaryToDecimal(value string) int {
	result, err := strconv.ParseInt(value, 2, 64)
	CheckError(err)
	return int(result)
}

func DecimalToBinary(decimal int) string {
	return strconv.FormatInt(int64(decimal), 2)
}

func HexToDecimal(hexadecimal string) int {
	result, err := strconv.ParseInt(hexadecimal, 16, 64)
	CheckError(err)
	return int(result)
}

func SubstringAfter(s, sep string) string {
	return strings.SplitN(s, sep, 2)[1]
}

func SplitAt(s string, split int) (string, string) {
	return s[:split], s[split+1:]
}

func IntCsv(s string) []int {
	var result []int
	for _, value := range strings.Split(s, ",") {
		result = append(result, ToInt(value))
	}
	return result
}

func Lines(s string) []string {
	return strings.Split(s, "\n")
}
