package util

import (
	"strconv"
	"strings"
)

func Must0(err error) {
	if err != nil {
		panic(err)
	}
}

func Must1[T any](value T, err error) T {
	Must0(err)
	return value
}

func Abs(value int) int {
	if value >= 0 {
		return value
	} else {
		return value * -1
	}
}

func HexDigest(hash [16]byte) []byte {
	var result [32]byte
	chars := "0123456789abcdef"
	for i, b := range hash {
		result[i*2+0] = chars[b>>4]
		result[i*2+1] = chars[b&0x0F]
	}
	return result[:]
}

func ToInt(value string) int {
	return Must1(strconv.Atoi(value))
}

func ToString(value int) string {
	return strconv.Itoa(value)
}

func ToDecimal(value string, base int) int {
	return int(Must1(strconv.ParseInt(value, base, 64)))
}

func DecimalToBinary(value int) string {
	return strconv.FormatInt(int64(value), 2)
}

func SubstringAfter(s, sep string) string {
	return strings.SplitN(s, sep, 2)[1]
}

func SplitAt(s string, split int) (string, string) {
	return s[:split], s[split+1:]
}

func IntCsv(s string) []int {
	return Map(strings.Split(s, ","), ToInt)
}

func Lines(s string) []string {
	return strings.Split(s, "\n")
}
